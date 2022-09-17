from rest_framework.viewsets import ViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin


class VersionedModelViewSet(ViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass


class ModelVersionViewSet(ViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    pass
