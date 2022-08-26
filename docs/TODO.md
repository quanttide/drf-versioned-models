# TODO

## 内部需求

允许直接访问ModelVersion的Field。比如`course.title`代替`courses.versions.latest('version').title`。

[自定义VersionMeta标记](tutorials/custom_version_meta.md)。支付服务的Price表需要自定义`related_name`为`prices`。

## 外部需求

[自定义`is_active`标记](tutorials/custom_is_active_field.md)。

## 不确定

`on_delete`选项不知道是否对关联逻辑的实现有什么影响，还需要评审。