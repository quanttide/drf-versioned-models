from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin


class VersionedModelViewSet(ModelViewSet):
    pass


class ReadOnlyVersionedModelViewSet(ReadOnlyModelViewSet):
    pass


class ModelVersionViewSet(ViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    pass


class ReadOnlyModelVersionViewSet(ReadOnlyModelViewSet):
    pass
