"""
测试数据模型
"""
import uuid

from django.db import models


# ----- Versioned models -----

class VersionedModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')


class VersionedModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    model = models.ForeignKey(VersionedModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    title = models.CharField(max_length=128, verbose_name='标题')


# ----- Nested versioned models -----

class ParentModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')


class ParentModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    model = models.ForeignKey(ParentModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    title = models.CharField(max_length=128, verbose_name='标题')


class ChildModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')
    parent = models.ForeignKey(ParentModel, related_name='children', on_delete=models.CASCADE, verbose_name='父模型')


class ChildModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    parent = models.ForeignKey(ParentModelVersion, related_name='children', on_delete=models.CASCADE, verbose_name='父模型')
    model = models.ForeignKey(VersionedModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    title = models.CharField(max_length=128, verbose_name='标题')


# ----- Multi versioned models -----

class MultiVersionedModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')


class Part1ModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    title = models.CharField(max_length=128, verbose_name='标题')


class Part2ModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    description = models.CharField(max_length=128, verbose_name='描述')