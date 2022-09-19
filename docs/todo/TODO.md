# TODO

## 内部需求

允许直接访问ModelVersion的Field。比如`course.title`代替`courses.versions.latest('version').title`。

定义QuerySet的delete方法。不知道怎么关联到Manager。

## 外部需求

[自定义`is_active`标记](custom_is_active_field.md)。

## 不确定

`on_delete`选项不知道是否对关联逻辑的实现有什么影响，还需要评审。

（重要）`PATCH`方法暂时不好定义。可行的思路是拉取上个版本并拼接，但目前的`POST`和`PUT`实际上允许更新多个版本，因此上述思路不太容易清晰定义。
