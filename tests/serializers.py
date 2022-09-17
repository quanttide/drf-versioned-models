from rest_framework import serializers

from drf_versioned_models.serializers import VersionedModelSerializer

from .models import *


class ExampleModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleModelVersion
        exclude = ['id', 'model', 'is_active']


class ExampleModelSerializer(VersionedModelSerializer):
    class Meta:
        model = ExampleModel
        exclude = ['is_active']

    class VersionMeta:
        version_serializer = ExampleModelVersionSerializer
        version_field = 'version'
        version_related_name = 'versions'
        version_field_mapping = {'created_at': 'updated_at'}
