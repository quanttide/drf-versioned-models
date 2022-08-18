from drf_versioned_models.serializers import VersionedModelSerializer

from .models import *


class ExampleModelSerializer(VersionedModelSerializer):
    class Meta:
        model = ExampleModel
        fields = "__all__"
        model_version = ExampleModelVersion
