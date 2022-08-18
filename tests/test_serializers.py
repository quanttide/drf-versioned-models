from django.test import TestCase

from tests.models import ExampleModel, ExampleModelVersion
from tests.serializers import ExampleModelSerializer


class VersionedModelSerializerTestCase(TestCase):
    serializer_class = ExampleModelSerializer

    def setUp(self):
        self.instance = ExampleModel.objects.create(name='test-instance')
        self.instance.versions.create(title='测试')
        self.new_data = {'name': 'test-name', 'title': '测试标题'}

    def test_to_representation(self):
        data = self.serializer_class.to_representation(self.instance)
        # TODO：查dict的单测验证语法

    def test_serialization(self):
        serializer = self.serializer_class(self.instance)
        self.assertTrue(serializer.data)

    def test_to_interval_value(self):
        expected_data = {'name': 'test-name', 'versions': [{'title': '测试标题'}]}
        processed_data = self.serializer_class.to_interval_value(self.data)
        # TODO：查dict的单测验证语法

    def test_validate(self):
        serializer = self.serializer_class(self.instance, data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create(self):
        serializer = self.serializer_class(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModel.objects.get(name=self.data['name']))
        self.assertTrue(ExampleModelVersion.objects.filter(title=self.data['title']).exists())

    def test_update(self):
        serializer = self.serializer_class(self.instance, data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModelVersion.objects.filter(title=self.data['title']).exists())
