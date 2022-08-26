# -*- coding: utf-8 -*-

from rest_framework import serializers


class VersionedModelSerializer(serializers.ModelSerializer):
    """
    版本化模型序列化类

    假设被序列化的模型由`Model`和`ModelVersion`的最新版本组成。
    其中`Model`定义不可变字段，`ModelVersion`定义可变字段。

    并且：
      - 关联命名为`versions`
      - `ModelVersion`的`created_at`作为`Model`的`updated_at`字段
      - `ModelVersion`的其他字段作为`Model`字段
    """

    class VersionMeta:
        version_serializer = None

    def to_representation(self, instance):
        """
        :param instance:
        :return:
        """
        instance_latest_version = instance.versions.latest('version')
        ret = super().to_representation(instance)
        ret.update(self.VersionMeta.version_serializer().to_representation(instance_latest_version))
        return ret

    def to_interval_value(self, data):
        return super().to_interval_value(data)

    @staticmethod
    def filter_allowed_fields(model, validated_data):
        """
        脚手架
        :param model:
        :param validated_data:
        :return:
        """
        allowed_fields = [field.name for field in model._meta.get_fields()]
        return {key: value for key, value in validated_data.items() if key in allowed_fields}

    def create_version(self, instance, validated_data):
        # https://docs.djangoproject.com/en/4.1/ref/models/relations/
        getattr(instance, self.Meta.model_version_related_name).create(**validated_data)
        return instance

    def create(self, validated_data):
        model = self.Meta.model
        model_version = self.Meta.model_version
        # 创建新模型
        instance = model.objects.create(**self.filter_allowed_fields(model, validated_data))
        # 创建新模型版本
        model_version_validated_data = self.filter_allowed_fields(model_version, validated_data)
        instance = self.create_version(instance, model_version_validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        更新模型定义为：
          - 使用现有模型不可变字段；
          - 创建模型版本及可变字段。

        :param instance:
        :param validated_data:
        :return:
        """
        model = self.Meta.model
        model_version = self.Meta.model_version
        # 创建新模型版本
        model_version_validated_data = self.filter_allowed_fields(model_version, validated_data)
        instance = self.create_version(instance, model_version_validated_data)
        return instance
