from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import (
    Addiction,
    AddictionKind,
    Attachment,
    ChatMessage,
    ChatParticipant,
    Dossier,
    Event,
    EventReference,
    NetworkSettings,
    Reference,
    Relationship,
    Share,
    Stance,
    Trait,
    Trust,
    TrustEntry,
    Visibility,
)


class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = ["uuid", "title", "created_at"]
        extra_kwargs = {"title": {"trim_whitespace": True, "allow_blank": False}}


class DossierPointsSerializer(DossierSerializer):
    points = serializers.IntegerField(read_only=True)

    class Meta(DossierSerializer.Meta):
        fields = [*DossierSerializer.Meta.fields, "points"]


class DossierDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = [
            "uuid",
            "title",
            "birthdate",
            "street",
            "postal_code",
            "canton",
            "nationality",
            "ethnicity",
        ]
        extra_kwargs = {"title": {"trim_whitespace": True, "allow_blank": False}}


class RelationshipSerializer(serializers.ModelSerializer):
    person = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Dossier.objects.all()
    )

    class Meta:
        model = Relationship
        fields = ["person", "status"]

    def validate_person(self, person):
        dossier = self.context["dossier"]
        if person == dossier:
            raise serializers.ValidationError(
                "Eine Akte kann nicht mit sich selbst verknüpft werden."
            )
        if Relationship.objects.between(dossier.uuid, person.uuid).exists():
            raise serializers.ValidationError("Diese Beziehung besteht bereits.")
        return person

    def to_representation(self, relationship):
        dossier = self.context["dossier"]
        return {
            "person": DossierSerializer(relationship.other(dossier)).data,
            "status": relationship.status_for(dossier),
        }


class NetworkSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkSettings
        fields = ["attraction", "distance", "repulsion", "gravity", "untangling"]


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ["uuid", "icon", "name", "url"]
        extra_kwargs = {"name": {"trim_whitespace": True, "allow_blank": False}}


class AddictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addiction
        fields = ["kind", "frequency"]

    def validate_kind(self, kind):
        if self.context["dossier"].addictions.of_kinds([kind]).exists():
            raise serializers.ValidationError("Diese Sucht ist bereits erfasst.")
        return kind


class StanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stance
        fields = ["topic", "tag"]


class TagsField(serializers.ListField):
    child = serializers.CharField(max_length=60, trim_whitespace=True)
    max_length = 30

    def to_internal_value(self, data):
        return list(dict.fromkeys(super().to_internal_value(data)))


class TopicStanceSerializer(serializers.Serializer):
    topic = serializers.CharField(read_only=True)
    tags = TagsField()
    value = serializers.IntegerField(read_only=True)
    suggestions = serializers.DictField(read_only=True)


class CharacterSerializer(serializers.Serializer):
    tags = TagsField()
    suggestions = serializers.DictField(read_only=True)


class EventSerializer(serializers.ModelSerializer):
    stances = StanceSerializer(many=True, read_only=True)
    traits = serializers.SlugRelatedField(many=True, read_only=True, slug_field="tag")
    addictions = AddictionSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)
    relationships = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "uuid",
            "title",
            "date",
            "stances",
            "traits",
            "addictions",
            "references",
            "relationships",
        ]
        extra_kwargs = {"title": {"trim_whitespace": True, "allow_blank": False}}

    def get_relationships(self, event):
        return RelationshipSerializer(
            event.relationships.all(), many=True, context={"dossier": event.dossier}
        ).data


class EventDetailSerializer(EventSerializer):
    trust = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        fields = [*EventSerializer.Meta.fields, "text", "trust", "updated_at"]
        extra_kwargs = {
            **EventSerializer.Meta.extra_kwargs,
            "text": {"trim_whitespace": False},
        }

    def get_trust(self, event):
        impact = TrustEntry.objects.impact(self.context["request"].user, event)
        return TrustImpactSerializer(impact).data


class EventLinksSerializer(serializers.Serializer):
    stances = StanceSerializer(many=True)
    traits = TagsField()
    addictions = serializers.ListField(
        child=serializers.ChoiceField(choices=AddictionKind.choices)
    )
    references = serializers.ListField(child=serializers.UUIDField())
    relationships = serializers.ListField(child=serializers.UUIDField())


class UUIDRelatedField(serializers.SlugRelatedField):
    def __init__(self, scope="reference", **kwargs):
        self.scope = scope
        super().__init__(slug_field="uuid", **kwargs)

    def get_queryset(self):
        return self.queryset.filter(**{self.scope: self.context[self.scope]})


class ChatParticipantSerializer(serializers.ModelSerializer):
    avatar = UUIDRelatedField(
        queryset=Attachment.objects.all(), allow_null=True, required=False
    )
    dossier = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Dossier.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ChatParticipant
        fields = ["uuid", "name", "side", "health", "avatar", "dossier"]
        extra_kwargs = {"name": {"trim_whitespace": True, "allow_blank": False}}

    def to_representation(self, participant):
        fight = self.context["fight"]
        return {
            **super().to_representation(participant),
            "dossier": participant.dossier
            and DossierSerializer(participant.dossier).data,
            "remaining": fight["health"].get(participant.pk, participant.health),
            "dealt": fight["dealt"][participant.pk],
        }


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UUIDRelatedField(queryset=ChatParticipant.objects.all())
    target = UUIDRelatedField(
        queryset=ChatParticipant.objects.all(), allow_null=True, required=False
    )
    image = UUIDRelatedField(
        queryset=Attachment.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = ChatMessage
        fields = ["uuid", "sender", "text", "image", "attack", "target"]
        extra_kwargs = {"text": {"trim_whitespace": False}}

    def validate(self, data):
        sender = data.get("sender", self.instance and self.instance.sender)
        target = data.get("target", self.instance and self.instance.target)
        if target and target == sender:
            raise serializers.ValidationError(
                {"target": "Man kann sich nicht selbst angreifen."}
            )
        return data

    def to_representation(self, message):
        return {
            **super().to_representation(message),
            "remaining": self.context["fight"]["remaining"].get(message.pk),
        }


class EventReferenceSerializer(serializers.ModelSerializer):
    links = UUIDRelatedField(
        scope="event",
        many=True,
        queryset=EventReference.objects.all(),
        required=False,
    )

    class Meta:
        model = EventReference
        fields = ["uuid", "kind", "icon", "title", "text", "links"]
        extra_kwargs = {
            "title": {"trim_whitespace": True, "allow_blank": False},
            "text": {"trim_whitespace": False},
        }

    def validate_links(self, links):
        if self.instance in links:
            raise serializers.ValidationError(
                "Eine Referenz kann nicht mit sich selbst verknüpft werden."
            )
        return links

    def to_representation(self, reference):
        context = {"fight": reference.fight()}
        return {
            **super().to_representation(reference),
            "participants": ChatParticipantSerializer(
                reference.participants.all(), many=True, context=context
            ).data,
            "messages": ChatMessageSerializer(
                reference.messages.all(), many=True, context=context
            ).data,
        }


class TrustSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dossier
        fields = ["uuid", "title", "level"]


class TrustLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trust
        fields = ["level"]


class TrustEntrySerializer(serializers.ModelSerializer):
    event = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Event.objects.all(),
        allow_null=True,
        required=False,
    )
    event_title = serializers.CharField(
        source="event.title", read_only=True, default=None
    )
    traits = TagsField(write_only=True, required=False)

    class Meta:
        model = TrustEntry
        fields = [
            "uuid",
            "conduct",
            "points",
            "date",
            "text",
            "event",
            "event_title",
            "traits",
        ]
        extra_kwargs = {"text": {"trim_whitespace": True, "allow_blank": False}}

    def create(self, validated_data):
        tags = validated_data.pop("traits", [])
        entry = super().create(validated_data)
        entry.traits.set(Trait.objects.ensure(entry.dossier, tags))
        return entry

    def to_representation(self, entry):
        return {
            **super().to_representation(entry),
            "traits": [trait.tag for trait in entry.traits.all()],
        }

    def validate_event(self, event):
        if event and event.dossier != self.context["dossier"]:
            raise serializers.ValidationError(
                "Das Ereignis gehört zu einer anderen Akte."
            )
        return event


class TrustLedgerSerializer(serializers.Serializer):
    points = serializers.IntegerField()
    level = serializers.IntegerField(allow_null=True)
    suggested_level = serializers.IntegerField(allow_null=True)
    conducts = serializers.DictField(child=serializers.IntegerField())
    conduct_traits = serializers.DictField(child=serializers.ListField())
    traits = serializers.ListField(child=serializers.CharField())
    entries = TrustEntrySerializer(many=True)


class TrustImpactSerializer(serializers.Serializer):
    points = serializers.IntegerField()
    entries = TrustEntrySerializer(many=True)


class ShareSerializer(serializers.ModelSerializer):
    recipient = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Dossier.objects.filter(govex_sub__isnull=False),
        allow_null=True,
        required=False,
        error_messages={"does_not_exist": "Diese Akte ist nicht mit govex verknüpft."},
    )
    password = serializers.CharField(
        write_only=True, required=False, allow_blank=True, max_length=128
    )
    has_password = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = Share
        fields = [
            "uuid",
            "recipient",
            "name",
            "token",
            "password",
            "has_password",
            "link",
            "created_at",
        ]
        extra_kwargs = {
            "name": {"trim_whitespace": True},
            "token": {
                "required": False,
                "validators": [
                    *Share._meta.get_field("token").validators,
                    UniqueValidator(
                        queryset=Share.objects.all(),
                        message="Dieser Pfad ist bereits vergeben.",
                    ),
                ],
            },
        }

    def validate_recipient(self, recipient):
        shares = self.context["dossier"].shares
        if recipient and shares.filter(recipient=recipient).exists():
            raise serializers.ValidationError("Diese Freigabe besteht bereits.")
        return recipient

    def validate(self, data):
        recipient = data.get("recipient", self.instance and self.instance.recipient)
        name = data.get("name", self.instance and self.instance.name)
        if not recipient and not name:
            raise serializers.ValidationError({"name": "Der Link braucht einen Namen."})
        return data

    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)
        share = super().save(**kwargs)
        if password is not None:
            share.set_password(password)
            share.save(update_fields=["password"])
        return share

    def get_has_password(self, share):
        return bool(share.password)

    def get_link(self, share):
        if share.recipient_id:
            return None
        base = f"{settings.MONOLITH_URL}/share/"
        return {"base": base, "url": f"{base}{share.token}"}

    def to_representation(self, share):
        return {
            **super().to_representation(share),
            "recipient": share.recipient and DossierSerializer(share.recipient).data,
        }


class ShareRulesSerializer(serializers.Serializer):
    rules = serializers.DictField(
        child=serializers.ChoiceField(choices=Visibility.choices)
    )

    def validate_rules(self, rules):
        if set(rules) - self.context["targets"]:
            raise serializers.ValidationError("Unbekannte Elemente.")
        return rules


class ShareAccessSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, allow_blank=True, max_length=128)
