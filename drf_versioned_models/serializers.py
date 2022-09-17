# -*- coding: utf-8 -*-

from rest_framework import serializers


class VersionedModelSerializer(serializers.ModelSerializer):
    """
    版本化模型序列化类

    假设被序列化的模型由`Model`和`ModelVersion`的最新版本组成。
    其中`Model`定义不可变字段，`ModelVersion`定义可变字段。

    ```python
    class CourseSerializer(VersionedModelSerializer):
        class VersionMeta:
            version_serializer = CourseVersionSerializer
            version_field_mapping = {
                'created_at': 'updated_at'
            }
    ```
    """

    class VersionMeta:
        version_serializer = None
        version_field_mapping = {}

    def _validate_duplicate_fields(self, data, version_data):
        duplicated_fields = set(data.keys()) & set(version_data.keys())
        if duplicated_fields:
            raise serializers.ValidationError("")
        return data, version_data

    def _replace_version_field(self, data):
        version_field_mapping = self.VersionMeta.version_field_mapping
        for key in data:
            if key in version_field_mapping:
                data[version_field_mapping[key]] = data.pop(key)
        return data

    def to_representation(self, instance):
        """
        :param instance:
        :return:
        """
        instance_latest_version = instance.versions.latest('version')
        ret = super().to_representation(instance)
        ret_version = self.VersionMeta.version_serializer().to_representation(instance_latest_version)
        # 版本字段冲突抛出异常，让开发者自己处理
        ret, ret_version = self._validate_duplicate_fields(ret, ret_version)
        # 处理版本字段名称更变，比如版本`created_at`改为`updated_at`
        ret_version = self._replace_version_field(ret_version)
        ret.update(ret_version)
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
