from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from shared.mixins.defaults import DefaultMixin
from shared.mixins.title import TitleMixin


class Instructor(DefaultMixin):
    author_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_object_id = models.PositiveIntegerField()

    author = GenericForeignKey('author_content_type', 'author_object_id')
    description = models.TextField()


class CourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(valid=True)

class Course(TitleMixin, DefaultMixin):
    objects = CourseManager()
    even_not_valid = models.Manager()

    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField('Category')
    valid = models.BooleanField(default=False)
    accept_guests = models.BooleanField(default=True)


class Category(TitleMixin, DefaultMixin):
    ...


class Class(TitleMixin, DefaultMixin):
    class Meta:
        verbose_name_plural = "Classes"

    duration = models.TimeField()
    video = models.FileField(upload_to='media/videos/')
    complementary = models.FileField(upload_to='media/complementary/')


class ClassViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    _class = models.ForeignKey('Class', on_delete=models.CASCADE)


class Exam(DefaultMixin):
    duration = models.TimeField()

class ExamViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

class Question(DefaultMixin):
    text = models.TextField()

class Options(DefaultMixin):
    text = models.TextField()
    correct = models.BooleanField()

class QuestionViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    option = models.ForeignKey('Question', on_delete=models.CASCADE)
