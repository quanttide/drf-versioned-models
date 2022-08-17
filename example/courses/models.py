import uuid

from django.db import models


class Course(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='课程ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='课程名称')


class CourseVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='课程版本ID')
    course = models.ForeignKey(Course, related_name='versions', on_delete=models.CASCADE, verbose_name='课程')
    title = models.CharField(max_length=128, verbose_name='课程名称')


class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='课时ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='课时名称')
    course = models.ForeignKey(Course, related_name='lectures', on_delete=models.CASCADE, verbose_name='课程')
    created_at = models.DateTimeField(verbose_name='课时创建时间')


class LectureVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='课时版本ID')
    course_version = models.ForeignKey(CourseVersion, related_name='lecture_versions', on_delete=models.CASCADE, verbose_name='课程版本')
    lecture = models.ForeignKey(Lecture, related_name='versions', on_delete=models.CASCADE, verbose_name='课时')
    updated_at = models.DateTimeField(default=None, verbose_name='课时版本更新时间')
    title = models.CharField(max_length=128, verbose_name='课时名称')