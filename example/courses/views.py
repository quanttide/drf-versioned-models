"""

"""

from drf_versioned_models.viewsets import VersionedModelViewSet, ModelVersionViewSet

from .models import Course, CourseVersion
from .serializers import CourseSerializer, CourseVersionSerializer


class CourseViewSet(VersionedModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseVersionViewSet(ModelVersionViewSet):
    queryset = CourseVersion.objects.all()
    serializer_class = CourseVersionSerializer


class LectureViewSet:
    pass
