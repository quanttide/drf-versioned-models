from django.test import TestCase

from drf_versioned_models.models import VersionedModel
from .models import ExampleModel, ExampleModelVersion


class VersionedModelTestCase(TestCase):
    model_class = ExampleModel
    fixtures = ['examples.json']

    def test_init(self):
        model_instance = self.model_class()
        self.assertIsInstance(model_instance, VersionedModel)
        self.assertTrue(model_instance.is_active)

    def test_get(self):
        model_instance = self.model_class.objects.get(name='data-analytics-with-python')
        self.assertEqual(model_instance.name, 'data-analytics-with-python')
        self.assertEqual(model_instance.versions.title, 'Python数据分析')

    def test_create(self):
        model_instance = self.model_class.objects.create(name='test', version='0.1.0', title='测试')
        self.assertEqual(model_instance.name, 'test')
        self.assertEqual(model_instance.versions.get(version='0.1.0'), '测试')

    def test_update(self):
        model_instance = self.model_class.objects.get(name='data-analytics-with-python')
        model_instance.objects.update(title='测试标题')
        self.assertEqual(model_instance.name, 'data-analytics-with-python')
        self.assertEqual(model_instance.versions.title, '测试标题')

    def test_delete(self):
        model_instance = self.model_class.objects.get()
        model_instance.delete()
        self.assertFalse(model_instance.is_active)


class ModelVersionTestCase(TestCase):
    model_class = ExampleModelVersion
    fixtures = ['examples.json']

    def test_init(self):
        pass

    def test_delete(self):
        model_instance = self.model_class.objects.get(version='0.1.0')
        model_instance.delete()
        # 似乎被真的删了，没发挥作用。
        # 这个还是原来的实例。
        self.assertFalse(model_instance.is_active)
