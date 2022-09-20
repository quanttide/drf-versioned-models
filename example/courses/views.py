"""

"""

from drf_versioned_models.viewsets import VersionedModelViewSet

from .models import Course, CourseVersion
from .serializers import CourseSerializer


class CourseViewSet(VersionedModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LectureViewSet:
    pass
