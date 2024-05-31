from django.db import models

class TitleMixin(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255)
    description = models.TextField()
