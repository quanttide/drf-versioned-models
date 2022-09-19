from rest_framework.serializers import ModelSerializer

from .models import Course, CourseVersion


class CourseVersionSerializer(ModelSerializer):
    class Meta:
        model = CourseVersion
        exclude = ['id', 'course', 'is_active']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        exclude = ['is_active']

    class VersionMeta:
        version_serializer = CourseVersionSerializer
        version_field = 'version'
        version_related_name = 'versions'
        version_field_mapping = {'created_at': 'updated_at'}
