from drf_versioned_models.viewsets import VersionedModelViewSet, ModelVersionViewSet

from .models import ExampleModel, ExampleModelVersion
from .serializers import ExampleModelSerializer, ExampleModelVersionSerializer


class ExampleModelViewSet(VersionedModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
    lookup_field = 'name'


class ExampleModelVersionViewSet(ModelVersionViewSet):
    queryset = ExampleModelVersion.objects.all()
    serializer_class = ExampleModelVersionSerializer


class LectureViewSet:
    pass
