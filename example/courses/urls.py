from rest_framework.routers import SimpleRouter
from example.courses.views import CourseViewSet


router = SimpleRouter()
router.register(r'courses', CourseViewSet)
urlpatterns = router.urls
