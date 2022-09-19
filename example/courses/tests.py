from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class CourseAPITestCase(APITestCase):
    def test_list_course(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
