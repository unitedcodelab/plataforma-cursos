from django.db import models
from django.contrib.contenttypes.models import ContentType

from shared.mixins.defaults import DefaultMixin
from shared.mixins.person import PersonMixin

from .extra_models.unit.students import UnitStudent


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(verified=True)

class Student(PersonMixin, DefaultMixin):
    objects = StudentManager()
    even_not_verified = models.Manager()

    enroll_number = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)


class Teacher(PersonMixin, DefaultMixin):
    ...


class Guest(PersonMixin, DefaultMixin):
    ...