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
    class Meta:
        # TODO: 自动查找关联关系
        model_version = None
        model_related_field = None

    def __init__(self, *args, **kwargs):
        self.validate_meta()
        super().__init__(*args, **kwargs)

    def validate_meta(self):
        # 验证Meta
        if not self.Meta.model_version:
            raise ValueError("请在Meta里设置model_version字段")
        if not self.Meta.model_related_field:
            raise ValueError("请在Meta里设置model_related_field字段")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 多个版本被序列化时，选取最新版本
        latest_version = ret.pop('versions')[-1]
        # 数据模型版本字段移到数据模型
        for key in latest_version:
            if key == 'created_at':
                # 版本发布时间作为数据模型更新时间
                ret['updated_at'] = latest_version[key]
            else:
                # 版本信息作为数据模型信息
                ret[key] = latest_version[key]
        return ret

    def to_interval_value(self, data):
        return super().to_interval_value(data)

    @staticmethod
    def filter_allowed_fields(model, validated_data):
        allowed_fields = [field.name for field in model._meta.get_fields()]
        return {key: value for key, value in validated_data.items() if key in allowed_fields}

    def create_version(self, instance, validated_data):
        pass

    def create(self, validated_data):
        model = self.Meta.model
        model_version = self.Meta.model_version
        # 创建新模型
        instance = model.objects.create(**self.filter_allowed_fields(model, validated_data))
        # 创建新模型版本
        model_version_validated_data = self.filter_allowed_fields(model_version, validated_data)
        model_version_validated_data.update({self.Meta.model_related_field: instance})
        model_version.objects.create(**model_version_validated_data)
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
        model_version_validated_data.update({self.Meta.model_related_field: instance})
        model_version.objects.create(**model_version_validated_data)
        return instance