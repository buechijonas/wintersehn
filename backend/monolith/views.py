from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from wintersehn.accounts.consent import push_to_govex

from . import govex, sharing, swissfy
from .models import (
    Addiction,
    Dossier,
    Event,
    NetworkSettings,
    Reference,
    Relationship,
    Share,
    Stance,
    Topic,
    Trust,
    TrustEntry,
)
from .permissions import CanViewMonolith, CanViewShared
from .serializers import (
    AddictionSerializer,
    DossierDetailSerializer,
    DossierPointsSerializer,
    DossierSerializer,
    EventDetailSerializer,
    EventLinksSerializer,
    EventSerializer,
    NetworkSettingsSerializer,
    ReferenceSerializer,
    RelationshipSerializer,
    ShareAccessSerializer,
    ShareRulesSerializer,
    ShareSerializer,
    TopicStanceSerializer,
    TrustEntrySerializer,
    TrustLedgerSerializer,
    TrustLevelSerializer,
    TrustSerializer,
)
from .throttling import ShareLinkIPThrottle, ShareLinkThrottle


class DossierListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        dossiers = TrustEntry.objects.points(request.user).filter(
            title__icontains=query
        )
        return Response(DossierPointsSerializer(dossiers, many=True).data)

    def post(self, request):
        serializer = DossierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DossierDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        return Response(
            DossierDetailSerializer(get_object_or_404(Dossier, uuid=uuid)).data
        )

    def patch(self, request, uuid):
        serializer = DossierDetailSerializer(
            get_object_or_404(Dossier, uuid=uuid), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RelationshipListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        relationships = Relationship.objects.of(dossier)
        return Response(
            RelationshipSerializer(
                relationships, many=True, context={"dossier": dossier}
            ).data
        )

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = RelationshipSerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RelationshipDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def patch(self, request, uuid, person):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        relationship = get_object_or_404(
            Relationship.objects.between(uuid, person).select_related(
                "dossier", "person"
            )
        )
        serializer = RelationshipSerializer(
            relationship,
            data={"status": request.data.get("status")},
            partial=True,
            context={"dossier": dossier},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier, person=relationship.other(dossier))
        return Response(serializer.data)

    def delete(self, request, uuid, person):
        get_object_or_404(Relationship.objects.between(uuid, person)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReferenceListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(ReferenceSerializer(dossier.references.all(), many=True).data)

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = ReferenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReferenceDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def delete(self, request, uuid, reference):
        get_object_or_404(Reference, dossier__uuid=uuid, uuid=reference).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddictionListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(AddictionSerializer(dossier.addictions.all(), many=True).data)

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = AddictionSerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddictionDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def patch(self, request, uuid, kind):
        addiction = get_object_or_404(
            Addiction.objects.of_kinds([kind]), dossier__uuid=uuid
        )
        serializer = AddictionSerializer(
            addiction, data={"frequency": request.data.get("frequency")}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid, kind):
        get_object_or_404(
            Addiction.objects.of_kinds([kind]), dossier__uuid=uuid
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        events = Event.objects.with_links().filter(dossier__uuid=uuid)
        return Response(EventSerializer(events, many=True).data)

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier, created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid, event):
        event = get_object_or_404(
            Event.objects.with_links(), dossier__uuid=uuid, uuid=event
        )
        return Response(EventDetailSerializer(event).data)

    def patch(self, request, uuid, event):
        event = get_object_or_404(Event, dossier__uuid=uuid, uuid=event)
        serializer = EventDetailSerializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid, event):
        get_object_or_404(Event, dossier__uuid=uuid, uuid=event).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventLinksView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def put(self, request, uuid, event):
        event = get_object_or_404(Event, dossier__uuid=uuid, uuid=event)
        serializer = EventLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event.link(**serializer.validated_data)
        return Response(EventDetailSerializer(event).data)


class StanceListView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(
            TopicStanceSerializer(Stance.objects.by_topic(dossier), many=True).data
        )


class StanceSummaryView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(Stance.objects.summary(dossier))


class StanceDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def put(self, request, uuid, topic):
        if topic not in Topic.values:
            raise Http404
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = TopicStanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stance = Stance.objects.set_tags(
            dossier, topic, serializer.validated_data["tags"]
        )
        return Response(TopicStanceSerializer(stance).data)


class NetworkView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request):
        relationships = Relationship.objects.values(
            "dossier__uuid", "person__uuid", "status"
        )
        return Response(
            {
                "dossiers": DossierSerializer(Dossier.objects.all(), many=True).data,
                "relationships": [
                    {
                        "dossier": relationship["dossier__uuid"],
                        "person": relationship["person__uuid"],
                        "status": relationship["status"],
                    }
                    for relationship in relationships
                ],
            }
        )


class NetworkSettingsView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request):
        network_settings = NetworkSettings.objects.filter(user=request.user).first()
        return Response(
            NetworkSettingsSerializer(network_settings or NetworkSettings()).data
        )

    def put(self, request):
        network_settings, _ = NetworkSettings.objects.get_or_create(user=request.user)
        serializer = NetworkSettingsSerializer(network_settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TrustView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request):
        dossiers = Trust.objects.circles(request.user)
        return Response(
            {
                "levels": Trust.LEVELS,
                "dossiers": TrustSerializer(dossiers, many=True).data,
            }
        )


class TrustDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def put(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = TrustLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Trust.objects.update_or_create(
            user=request.user, dossier=dossier, defaults=serializer.validated_data
        )
        return Response(serializer.data)

    def delete(self, request, uuid):
        Trust.objects.filter(user=request.user, dossier__uuid=uuid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def ledger(user, dossier):
    return TrustLedgerSerializer(TrustEntry.objects.ledger(user, dossier)).data


class TrustEntryListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(ledger(request.user, dossier))

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = TrustEntrySerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, dossier=dossier)
        return Response(ledger(request.user, dossier), status=status.HTTP_201_CREATED)


class TrustEntryDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def delete(self, request, uuid, entry):
        entry = get_object_or_404(
            TrustEntry, user=request.user, dossier__uuid=uuid, uuid=entry
        )
        entry.delete()
        return Response(ledger(request.user, entry.dossier))


class ShareListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        recipients = Dossier.objects.filter(govex_sub__isnull=False).exclude(
            received_shares__dossier=dossier
        )
        return Response(
            {
                "shares": ShareSerializer(
                    dossier.shares.select_related("recipient"), many=True
                ).data,
                "recipients": DossierSerializer(recipients, many=True).data,
            }
        )

    def post(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        serializer = ShareSerializer(data=request.data, context={"dossier": dossier})
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier, created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShareDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def share(self, uuid, share):
        return get_object_or_404(
            Share.objects.select_related("dossier", "recipient", "created_by"),
            dossier__uuid=uuid,
            uuid=share,
        )

    def response(self, share):
        return Response({**ShareSerializer(share).data, **sharing.editable(share)})

    def get(self, request, uuid, share):
        return self.response(self.share(uuid, share))

    def patch(self, request, uuid, share):
        share = self.share(uuid, share)
        serializer = ShareSerializer(
            share,
            data=request.data,
            partial=True,
            context={"dossier": share.dossier},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.response(share)

    def put(self, request, uuid, share):
        share = self.share(uuid, share)
        serializer = ShareRulesSerializer(
            data=request.data, context={"targets": sharing.targets(share)}
        )
        serializer.is_valid(raise_exception=True)
        share.set_rules(serializer.validated_data["rules"])
        return self.response(share)

    def delete(self, request, uuid, share):
        self.share(uuid, share).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharePreviewView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid, share):
        share = get_object_or_404(Share, dossier__uuid=uuid, uuid=share)
        return Response(sharing.redacted(share))


class SharedListView(APIView):
    permission_classes = [IsAuthenticated, CanViewShared]

    def get(self, request):
        shares = Share.objects.received_by(request.user)
        return Response(
            [
                {"uuid": share.uuid, "title": sharing.shared_title(share)}
                for share in shares
            ]
        )


class SharedDetailView(APIView):
    permission_classes = [IsAuthenticated, CanViewShared]

    def get(self, request, share):
        share = get_object_or_404(Share.objects.received_by(request.user), uuid=share)
        return Response(sharing.redacted(share))


class SharedLinkView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ShareLinkIPThrottle, ShareLinkThrottle]

    def post(self, request, token):
        share = get_object_or_404(Share.objects.links(), token=token)
        serializer = ShareAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not share.check_password(serializer.validated_data.get("password", "")):
            return Response(
                {"password_required": True},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(sharing.redacted(share))


class GovexSearchView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        return Response(govex.search_accounts(query) if len(query) >= 2 else [])


class DossierGovexView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        account = dossier.govex_sub and govex.get_account(dossier.govex_sub)
        return Response({"linked": bool(dossier.govex_sub), "account": account or None})

    def put(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        sub = str(request.data.get("sub", ""))
        account = sub and govex.get_account(sub)
        if not account:
            raise ValidationError({"detail": "Dieses govex-Konto existiert nicht."})
        other = Dossier.objects.filter(govex_sub=sub).exclude(pk=dossier.pk).first()
        if other:
            raise ValidationError(
                {"detail": f"Bereits mit der Akte «{other.title}» verknüpft."}
            )
        previous = dossier.govex_sub
        dossier.govex_sub = sub
        dossier.save(update_fields=["govex_sub"])
        push_to_govex(sub)
        if previous != sub:
            push_to_govex(previous)
        return Response({"linked": True, "account": account})

    def delete(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        previous = dossier.govex_sub
        dossier.govex_sub = None
        dossier.save(update_fields=["govex_sub"])
        push_to_govex(previous)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DossierSwissfyView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid)
        return Response(
            {
                "profile": dossier.govex_sub
                and swissfy.get_profile(dossier.govex_sub)
                or None
            }
        )


class DossierSwissfyPictureView(APIView):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def get(self, request, uuid):
        dossier = get_object_or_404(Dossier, uuid=uuid, govex_sub__isnull=False)
        picture = swissfy.get_picture(dossier.govex_sub)
        if not picture:
            raise Http404
        response = HttpResponse(
            picture.content, content_type=picture.headers.get("Content-Type")
        )
        response["Cache-Control"] = "private, max-age=300"
        return response
