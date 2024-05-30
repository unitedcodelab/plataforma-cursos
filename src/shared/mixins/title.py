from django.db import models
from .defaults import DefaultMixin

class TitleMixin(DefaultMixin):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
