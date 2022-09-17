from django.test import TestCase

from tests.models import ExampleModel, ExampleModelVersion
from tests.serializers import ExampleModelSerializer


class VersionedModelSerializerTestCase(TestCase):
    serializer_class = ExampleModelSerializer
    fixtures = ['examples.json']

    def setUp(self):
        self.instance = ExampleModel.objects.get(name='data-analytics-with-python')
        self.serialized_data = {
            'id': "61741d93-8db4-4845-83c9-7e625e445983",
            'name': 'data-analytics-with-python',
            'version': '0.1.0',
            "title": "Python数据分析",
            "updated_at": '2022-05-23T00:00:00'
        }
        self.new_data = {'name': 'test-name', 'title': '测试标题', 'version': '0.1.0'}

    def test_to_representation(self):
        data = self.serializer_class().to_representation(self.instance)
        self.assertDictEqual(self.serialized_data, dict(data))

    def test_serialization(self):
        serializer = self.serializer_class(self.instance)
        self.assertDictEqual(self.serialized_data, serializer.data)

    def test_to_interval_value(self):
        expected_data = {'name': 'test-name', 'versions': [{'title': '测试标题'}]}
        processed_data = self.serializer_class.to_interval_value(self.new_data)
        # TODO：查dict的单测验证语法

    def test_validate(self):
        serializer = self.serializer_class(self.instance, data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create(self):
        serializer = self.serializer_class(data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModel.objects.get(name=self.new_data['name']))
        self.assertTrue(ExampleModelVersion.objects.filter(title=self.new_data['title']).exists())

    def test_update(self):
        serializer = self.serializer_class(self.instance, data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModelVersion.objects.filter(title=self.new_data['title']).exists())
