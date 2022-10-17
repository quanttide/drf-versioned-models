# TODO

## v0.1.2

优化`is_active=False`的处理

ViewSet类：
- 响应状态增加410状态码。
- `list`方法留下`is_active=True`。

## v0.2.0

增加版本模型的子模型及API。

子模型的定义是，不独立进行版本号管理，而是跟随模型的版本更新。
比如示例项目`courses`应用的`Lecture`模型。

通过定义Router类把子模型的API和模型一起暴露。
主要通过封装`NestedSimpleRouter`类实现。

## 测试

引入tox。参考[`drf-nested-router`](https://github.com/alanjds/drf-nested-routers)。

## 其他

### 优化模型类查询

允许`VersionedModel`直接访问ModelVersion的Field。比如`course.title`代替`courses.versions.latest('version').title`。

### 优化序列化类默认过滤字段

Version表的`id`字段、关联Model的字段一般可以不要。

### 允许用户定义`is_active`字段

有两种可能的场景下，用户需要自定义名称和真假。

1. 用户已经有一个定义为`is_active`的字段，引入以后会导致冲突。
2. 用户已经有一个类似功能的相反的定义，比如`is_deprecated`、`is_removed`，希望尽可能兼容地接入。

### 规范`Meta`类

由于Django的Model类限制Meta传参未定义字段，抛出如下异常。

```python
>>> TypeError: 'class Meta' got invalid attribute(s)
```

为了非侵入地解决这个问题，我们可以创建新的Meta类（比如`VersionMeta`）实现我们需要的功能，
参考https://stackoverflow.com/questions/1088431/adding-attributes-into-django-models-meta-class。

但这样不一定规范，因此暂时把逻辑转移到序列化类实现（序列化类无此限制），后续根据实际情况决定。
