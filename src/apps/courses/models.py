from math import ceil

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from shared.mixins.defaults import DefaultMixin, SlugMixin
from shared.mixins.title import TitleMixin


class Instructor(DefaultMixin):
    author_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    author_object_id = models.PositiveIntegerField()

    author = GenericForeignKey('author_content_type', 'author_object_id')
    description = models.TextField()


class CourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(valid=True)

class Course(TitleMixin, DefaultMixin, SlugMixin):
    def upload_to(instance, filename):
        return f'media/courses/{instance.slug}/{filename}'

    objects = CourseManager()
    even_not_valid = models.Manager()

    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField('Category')
    thumbnail = models.ImageField(upload_to=upload_to)
    valid = models.BooleanField(default=False)
    accept_guests = models.BooleanField(default=True)

    def get_hours(self) -> float:
        hours = sum([c.duration.hour for c in self.classes.all()])
        minutes =  sum([c.duration.minute for c in self.classes.all()])
        return ceil(hours + minutes / 60)

    def __str__(self):
        return self.title

class Category(TitleMixin, DefaultMixin):
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.title


class Class(TitleMixin, DefaultMixin, SlugMixin):
    class Meta:
        verbose_name_plural = "Classes"
    

    def classes_upload_to(instance, filename):
        return f'media/classes/{instance.slug}/videos/{filename}'

    def complementaries_upload_to(instance, filename):
        return f'media/classes/{instance.slug}/complementaries/{filename}'


    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='classes')
    duration = models.TimeField()
    video = models.FileField(upload_to=classes_upload_to)
    complementary = models.FileField(upload_to=complementaries_upload_to)


    def __str__(self):
        return self.title
    

class ClassViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    _class = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='viewers')

    def __str__(self):
        return f"{self.viewer} - {self._class}"


class Exam(DefaultMixin):
    duration = models.TimeField()

class ExamViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

class Question(DefaultMixin):
    text = models.TextField()

class Option(DefaultMixin):
    text = models.TextField()
    correct = models.BooleanField()

class QuestionViewer(DefaultMixin):
    viewer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewer_object_id = models.PositiveIntegerField()

    viewer = GenericForeignKey('viewer_content_type', 'viewer_object_id')
    option = models.ForeignKey('Question', on_delete=models.CASCADE)


class Certificate(DefaultMixin):
    def upload_to(instance, filename):
        return f'media/certificados/{instance.student.name}/{filename}'

    student_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    student_object_id = models.PositiveIntegerField()

    student = GenericForeignKey('student_content_type', 'student_object_id')
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    file = models.FileField(upload_to=upload_to)
