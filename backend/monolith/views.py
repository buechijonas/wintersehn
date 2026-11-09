from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from commons import images, markdown
from commons.serializers import MarkdownPreviewSerializer
from commons.views import BaseViewSet
from wintersehn.accounts.consent import push_to_govex

from . import govex, sharing, swissfy
from .models import (
    Addiction,
    ChatImage,
    Dossier,
    Event,
    EventReference,
    NetworkSettings,
    Reference,
    Relationship,
    Share,
    Stance,
    Topic,
    Trait,
    Trust,
    TrustEntry,
)
from .permissions import CanViewMonolith, CanViewShared
from .serializers import (
    AddictionSerializer,
    CharacterSerializer,
    ChatImageSerializer,
    ChatMessageSerializer,
    ChatParticipantSerializer,
    DossierDetailSerializer,
    DossierPointsSerializer,
    DossierSerializer,
    EventDetailSerializer,
    EventLinksSerializer,
    EventReferenceSerializer,
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


class MonolithViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, CanViewMonolith]

    def dossier(self, **lookup):
        dossiers = Dossier.objects.apply_acl(self.request.user)
        return get_object_or_404(dossiers, uuid=self.kwargs["uuid"], **lookup)


class DossierViewSet(MonolithViewSet):
    def list(self, request):
        query = request.query_params.get("q", "").strip()
        dossiers = TrustEntry.objects.points(request.user).filter(
            title__icontains=query
        )
        return Response(DossierPointsSerializer(dossiers, many=True).data)

    def create(self, request):
        serializer = DossierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, uuid):
        return Response(DossierDetailSerializer(self.dossier()).data)

    def partial_update(self, request, uuid):
        serializer = DossierDetailSerializer(
            self.dossier(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RelationshipViewSet(MonolithViewSet):
    def list(self, request, uuid):
        dossier = self.dossier()
        relationships = Relationship.objects.of(dossier)
        return Response(
            RelationshipSerializer(
                relationships, many=True, context={"dossier": dossier}
            ).data
        )

    def create(self, request, uuid):
        dossier = self.dossier()
        serializer = RelationshipSerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, uuid, person):
        dossier = self.dossier()
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

    def destroy(self, request, uuid, person):
        get_object_or_404(Relationship.objects.between(uuid, person)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReferenceViewSet(MonolithViewSet):
    def list(self, request, uuid):
        return Response(
            ReferenceSerializer(self.dossier().references.all(), many=True).data
        )

    def create(self, request, uuid):
        serializer = ReferenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=self.dossier())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, uuid, reference):
        get_object_or_404(Reference, dossier__uuid=uuid, uuid=reference).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddictionViewSet(MonolithViewSet):
    def addiction(self, kind):
        return get_object_or_404(
            Addiction.objects.of_kinds([kind]), dossier__uuid=self.kwargs["uuid"]
        )

    def list(self, request, uuid):
        return Response(
            AddictionSerializer(self.dossier().addictions.all(), many=True).data
        )

    def create(self, request, uuid):
        dossier = self.dossier()
        serializer = AddictionSerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, uuid, kind):
        serializer = AddictionSerializer(
            self.addiction(kind),
            data={"frequency": request.data.get("frequency")},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, uuid, kind):
        self.addiction(kind).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventViewSet(MonolithViewSet):
    def event(self):
        return get_object_or_404(
            Event.objects.with_links(),
            dossiers__uuid=self.kwargs["uuid"],
            uuid=self.kwargs["event"],
        )

    def context(self):
        return {"request": self.request, "dossier": self.dossier()}

    def respond(self, event, status_code=status.HTTP_200_OK):
        event = Event.objects.with_links().get(pk=event.pk)
        return Response(
            EventDetailSerializer(event, context=self.context()).data,
            status=status_code,
        )

    def list(self, request, uuid):
        events = Event.objects.with_links().filter(dossiers__uuid=uuid)
        return Response(EventSerializer(events, many=True, context=self.context()).data)

    def create(self, request, uuid):
        context = self.context()
        serializer = EventSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        event = serializer.save(created_by=request.user)
        event.dossiers.add(context["dossier"])
        return self.respond(event, status.HTTP_201_CREATED)

    def retrieve(self, request, uuid, event):
        return self.respond(self.event())

    def partial_update(self, request, uuid, event):
        serializer = EventDetailSerializer(
            self.event(), data=request.data, partial=True, context=self.context()
        )
        serializer.is_valid(raise_exception=True)
        return self.respond(serializer.save())

    def destroy(self, request, uuid, event):
        self.event().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def links(self, request, uuid, event):
        event = self.event()
        serializer = EventLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event.link(self.dossier(), **serializer.validated_data)
        return self.respond(event)


class EventReferenceViewSet(MonolithViewSet):
    def reference(self):
        return get_object_or_404(
            EventReference,
            event__dossiers__uuid=self.kwargs["uuid"],
            event__uuid=self.kwargs["event"],
            uuid=self.kwargs["reference"],
        )

    def respond(self, reference, status_code=status.HTTP_200_OK):
        reference = EventReference.objects.with_chat().get(pk=reference.pk)
        return Response(EventReferenceSerializer(reference).data, status=status_code)

    def list(self, request, uuid, event):
        references = EventReference.objects.with_chat().filter(
            event__dossiers__uuid=uuid, event__uuid=event
        )
        return Response(EventReferenceSerializer(references, many=True).data)

    def create(self, request, uuid, event):
        event = get_object_or_404(Event, dossiers__uuid=uuid, uuid=event)
        serializer = EventReferenceSerializer(
            data=request.data, context={"event": event}
        )
        serializer.is_valid(raise_exception=True)
        return self.respond(serializer.save(event=event), status.HTTP_201_CREATED)

    def retrieve(self, request, uuid, event, reference):
        return self.respond(self.reference())

    def partial_update(self, request, uuid, event, reference):
        reference = self.reference()
        serializer = EventReferenceSerializer(
            reference,
            data=request.data,
            partial=True,
            context={"event": reference.event},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.respond(reference)

    def destroy(self, request, uuid, event, reference):
        self.reference().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatItemViewSet(EventReferenceViewSet):
    item_serializer = None

    def item(self, reference):
        model = self.item_serializer.Meta.model
        return get_object_or_404(model, reference=reference, uuid=self.kwargs["item"])

    def create(self, request, uuid, event, reference):
        reference = self.reference()
        serializer = self.item_serializer(
            data=request.data, context={"reference": reference}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(reference=reference)
        return self.respond(reference, status.HTTP_201_CREATED)

    def partial_update(self, request, uuid, event, reference, item):
        reference = self.reference()
        serializer = self.item_serializer(
            self.item(reference),
            data=request.data,
            partial=True,
            context={"reference": reference},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.respond(reference)

    def destroy(self, request, uuid, event, reference, item):
        reference = self.reference()
        self.item(reference).delete()
        return self.respond(reference)


class ChatParticipantViewSet(ChatItemViewSet):
    item_serializer = ChatParticipantSerializer


class ChatMessageViewSet(ChatItemViewSet):
    item_serializer = ChatMessageSerializer


class ChatImageViewSet(MonolithViewSet):
    parser_classes = [MultiPartParser]

    def list(self, request):
        return Response(
            ChatImageSerializer(ChatImage.objects.with_usage(), many=True).data
        )

    def create(self, request):
        upload = request.FILES.get("file")
        if not upload:
            raise ValidationError({"file": "Keine Datei hochgeladen."})
        name = request.data.get("name", "").strip() or images.name(upload)
        image = ChatImage.objects.store(name, images.encode(upload), request.user)
        image = ChatImage.objects.with_usage().get(pk=image.pk)
        return Response(ChatImageSerializer(image).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, image):
        image = get_object_or_404(ChatImage, uuid=image)
        size = request.query_params.get("size", "")
        data = images.thumbnail(image.data, int(size) if size.isdigit() else None)
        response = HttpResponse(data, content_type="image/webp")
        response["Cache-Control"] = "private, max-age=86400"
        return response

    def partial_update(self, request, image):
        image = get_object_or_404(ChatImage.objects.with_usage(), uuid=image)
        serializer = ChatImageSerializer(image, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, image):
        get_object_or_404(ChatImage, uuid=image).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def unused(self, request):
        ChatImage.objects.filter(
            pk__in=ChatImage.objects.unused().values("pk")
        ).delete()
        return self.list(request)


class CharacterViewSet(MonolithViewSet):
    def retrieve(self, request, uuid):
        return Response(
            CharacterSerializer(Trait.objects.character(self.dossier())).data
        )

    def update(self, request, uuid):
        serializer = CharacterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character = Trait.objects.set_tags(
            self.dossier(), serializer.validated_data["tags"]
        )
        return Response(CharacterSerializer(character).data)


class StanceViewSet(MonolithViewSet):
    def list(self, request, uuid):
        return Response(
            TopicStanceSerializer(
                Stance.objects.by_topic(self.dossier()), many=True
            ).data
        )

    def summary(self, request, uuid):
        return Response(Stance.objects.summary(self.dossier()))

    def update(self, request, uuid, topic):
        if topic not in Topic.values:
            raise Http404
        serializer = TopicStanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stance = Stance.objects.set_tags(
            self.dossier(), topic, serializer.validated_data["tags"]
        )
        return Response(TopicStanceSerializer(stance).data)


class NetworkViewSet(MonolithViewSet):
    def list(self, request):
        relationships = Relationship.objects.values(
            "dossier__uuid", "person__uuid", "status"
        )
        return Response(
            {
                "dossiers": DossierSerializer(
                    Dossier.objects.apply_acl(request.user), many=True
                ).data,
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

    def network_settings(self):
        return NetworkSettings.objects.filter(user=self.request.user).first()

    def retrieve(self, request):
        return Response(
            NetworkSettingsSerializer(self.network_settings() or NetworkSettings()).data
        )

    def update(self, request):
        network_settings = self.network_settings() or NetworkSettings(user=request.user)
        serializer = NetworkSettingsSerializer(network_settings, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TrustViewSet(MonolithViewSet):
    def ledger(self, dossier):
        return TrustLedgerSerializer(
            TrustEntry.objects.ledger(self.request.user, dossier)
        ).data

    def list(self, request):
        dossiers = Trust.objects.circles(request.user)
        return Response(
            {
                "levels": Trust.LEVELS,
                "dossiers": TrustSerializer(dossiers, many=True).data,
            }
        )

    def update(self, request, uuid):
        serializer = TrustLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Trust.objects.update_or_create(
            user=request.user,
            dossier=self.dossier(),
            defaults=serializer.validated_data,
        )
        return Response(serializer.data)

    def destroy(self, request, uuid):
        Trust.objects.filter(user=request.user, dossier__uuid=uuid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def entries(self, request, uuid):
        return Response(self.ledger(self.dossier()))

    def add_entry(self, request, uuid):
        dossier = self.dossier()
        serializer = TrustEntrySerializer(
            data=request.data, context={"dossier": dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, dossier=dossier)
        return Response(self.ledger(dossier), status=status.HTTP_201_CREATED)

    def remove_entry(self, request, uuid, entry):
        entry = get_object_or_404(
            TrustEntry, user=request.user, dossier__uuid=uuid, uuid=entry
        )
        entry.delete()
        return Response(self.ledger(entry.dossier))


class ShareViewSet(MonolithViewSet):
    def share(self):
        return get_object_or_404(
            Share.objects.select_related("dossier", "recipient", "created_by"),
            dossier__uuid=self.kwargs["uuid"],
            uuid=self.kwargs["share"],
        )

    def respond(self, share):
        return Response({**ShareSerializer(share).data, **sharing.editable(share)})

    def list(self, request, uuid):
        dossier = self.dossier()
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

    def create(self, request, uuid):
        dossier = self.dossier()
        serializer = ShareSerializer(data=request.data, context={"dossier": dossier})
        serializer.is_valid(raise_exception=True)
        serializer.save(dossier=dossier, created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, uuid, share):
        return self.respond(self.share())

    def partial_update(self, request, uuid, share):
        share = self.share()
        serializer = ShareSerializer(
            share, data=request.data, partial=True, context={"dossier": share.dossier}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.respond(share)

    def update(self, request, uuid, share):
        share = self.share()
        serializer = ShareRulesSerializer(
            data=request.data, context={"targets": sharing.targets(share)}
        )
        serializer.is_valid(raise_exception=True)
        share.set_rules(serializer.validated_data["rules"])
        return self.respond(share)

    def destroy(self, request, uuid, share):
        self.share().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def preview(self, request, uuid, share):
        return Response(
            sharing.redacted(get_object_or_404(Share, dossier__uuid=uuid, uuid=share))
        )


class SharedViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated, CanViewShared]

    def list(self, request):
        return Response(
            [
                {"uuid": share.uuid, "title": sharing.shared_title(share)}
                for share in Share.objects.received_by(request.user)
            ]
        )

    def retrieve(self, request, share):
        share = get_object_or_404(Share.objects.received_by(request.user), uuid=share)
        return Response(sharing.redacted(share))


class SharedLinkViewSet(BaseViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ShareLinkIPThrottle, ShareLinkThrottle]

    def create(self, request, token):
        share = get_object_or_404(Share.objects.links(), token=token)
        serializer = ShareAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not share.check_password(serializer.validated_data.get("password", "")):
            return Response(
                {"password_required": True}, status=status.HTTP_403_FORBIDDEN
            )
        return Response(sharing.redacted(share))


class GovexViewSet(MonolithViewSet):
    def list(self, request):
        query = request.query_params.get("q", "").strip()
        return Response(govex.search_accounts(query) if len(query) >= 2 else [])

    def retrieve(self, request, uuid):
        dossier = self.dossier()
        account = dossier.govex_sub and govex.get_account(dossier.govex_sub)
        return Response({"linked": bool(dossier.govex_sub), "account": account or None})

    def update(self, request, uuid):
        dossier = self.dossier()
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

    def destroy(self, request, uuid):
        dossier = self.dossier()
        previous = dossier.govex_sub
        dossier.govex_sub = None
        dossier.save(update_fields=["govex_sub"])
        push_to_govex(previous)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwissfyViewSet(MonolithViewSet):
    def retrieve(self, request, uuid):
        dossier = self.dossier()
        return Response(
            {
                "profile": dossier.govex_sub
                and swissfy.get_profile(dossier.govex_sub)
                or None
            }
        )

    def picture(self, request, uuid):
        dossier = self.dossier(govex_sub__isnull=False)
        picture = swissfy.get_picture(dossier.govex_sub)
        if not picture:
            raise Http404
        response = HttpResponse(
            picture.content, content_type=picture.headers.get("Content-Type")
        )
        response["Cache-Control"] = "private, max-age=300"
        return response


class MarkdownViewSet(MonolithViewSet):
    def preview(self, request):
        serializer = MarkdownPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"html": markdown.render(serializer.validated_data["body"])})
