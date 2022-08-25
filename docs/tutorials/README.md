# 用户文档

## 定义模型

把计划版本管理的模型分为不可变部分和可变部分，其中：
- 不可变部分继承`VersionedModel`类。
- 可变部分继承`ModelVersion`类，关联上述模型的字段的`related_name`设置成`versions`。

比如：
```python
from djang.db import models
from drf_versioned_models.models import VersionedModel, ModelVersion


class MyModel(VersionedModel):
    pass

class MyModelVersion(ModelVersion):
    model = models.ForeignKey(MyModel, related_name='versions', on_delete=models.CASCADE)
```

你可以通过[自定义这两个类的`VersionMeta`类](custom_version_meta.md)来实现。

## 定义API

### 模型API

`/{model_class}s/{lookup_field}/`

- `GET`: 获取最新版本的单个或者列表。
- `POST`: 创建模型及版本。
- `PUT`/`PATCH`: 创建新版本，内部逻辑是拉取上一个版本并拼接。
- `DELETE`: "删除"模型，实际上是标记`is_active=False`。

### 模型版本API

`/<model_class>s/{lookup_field}/<version_related_name>/{version}`

- `GET`: 获取全部版本，或者根据版本号字段某个版本。
- `POST`: 创建版本。
- `DELETE`: "删除"版本，实际上是标记`is_active=False`。
- `PUT`和`PATCH`不支持。
