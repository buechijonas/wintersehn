from rest_framework import serializers

READ_ACTIONS = {"list", "retrieve"}


class BaseModelSerializer:
    list = None
    retrieve = None

    class read(serializers.ModelSerializer):
        class Meta:
            fields = []

    class write(serializers.ModelSerializer):
        class Meta:
            fields = []

    @classmethod
    def for_action(cls, action):
        if action == "list":
            return cls.list or cls.read
        if action in READ_ACTIONS:
            return cls.retrieve or cls.read
        return cls.write


class MarkdownPreviewSerializer(serializers.Serializer):
    body = serializers.CharField(allow_blank=True, trim_whitespace=False)


class UUIDModelSerializer(BaseModelSerializer):
    class read(BaseModelSerializer.read):
        class Meta(BaseModelSerializer.read.Meta):
            fields = ["uuid"]
