from django.test import TestCase
from django.urls import include, path, reverse, resolve

from rest_framework.test import URLPatternsTestCase
from rest_framework.status import HTTP_200_OK


class VersionedModelRouterTestCase(TestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('tests.urls'))
    ]

    def test_reverse_example_model_list_url(self):
        url = reverse('tests:examplemodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_resolve_example_model_list_url(self):
        match = resolve('/examples/')
        self.assertEqual(match.view_name, 'tests:examplemodel-list')
