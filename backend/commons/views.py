from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class BaseViewSet(viewsets.GenericViewSet):
    permission_action_classes = {}

    def get_queryset(self):
        raise NotImplementedError()

    def get_serializer_class(self):
        return super().get_serializer_class().for_action(self.action)

    def get_permissions(self):
        classes = self.permission_action_classes.get(
            self.action, self.permission_classes
        )
        return [permission() for permission in classes]

    def read(self, instance, status_code=status.HTTP_200_OK):
        instance = self.get_queryset().get(pk=instance.pk)
        serializer_class = self.serializer_class.for_action("retrieve")
        serializer = serializer_class(instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status_code)


class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.read(self.perform_create(serializer), status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()


class UpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        return self.read(self.perform_update(serializer))

    def perform_update(self, serializer):
        return serializer.save()
