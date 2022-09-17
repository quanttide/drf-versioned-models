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
        # 仅做样例，实际上不会被直接继承
        version_serializer = None
        version_field = 'version'
        version_related_name = 'versions'
        version_field_mapping = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 版本字段冲突抛出异常，让开发者自己处理
        self._validate_duplicate_fields()

    def _validate_duplicate_fields(self):
        model_fields = self.get_fields().keys()
        model_version_fields = self.VersionMeta.version_serializer().get_fields().keys()
        duplicated_fields = set(model_fields) & set(model_version_fields)
        if duplicated_fields:
            raise serializers.ValidationError("未处理重复字段")

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
        instance_latest_version = instance.versions.latest(self.VersionMeta.version_field)
        ret = super().to_representation(instance)
        ret_version = self.VersionMeta.version_serializer().to_representation(instance_latest_version)
        # 处理版本字段名称更变，比如版本`created_at`改为`updated_at`
        ret_version = self._replace_version_field(ret_version)
        ret.update(ret_version)
        return ret

    def to_internal_value(self, data):
        data[self.VersionMeta.version_related_name] = self.initial_data[self.VersionMeta.version_related_name]
        return data

    def create(self, validated_data):
        # 取出版本数据
        version_validated_data_list = validated_data.pop(self.VersionMeta.version_related_name)
        # 创建新模型
        instance = self.Meta.model.objects.create(**validated_data)
        # 创建新模型版本
        for version_validated_data in version_validated_data_list:
            getattr(instance, self.VersionMeta.version_related_name).create(**version_validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        更新模型定义为：
          - 使用现有模型不可变字段（TODO：验证模型不变，具体异常方式待定义）
          - 创建模型版本及可变字段

        :param instance:
        :param validated_data:
        :return:
        """
        # 取出版本数据
        version_validated_data_list = validated_data.pop(self.VersionMeta.version_related_name)
        # 创建新模型版本
        for version_validated_data in version_validated_data_list:
            getattr(instance, self.VersionMeta.version_related_name).create(**version_validated_data)
        return instance
