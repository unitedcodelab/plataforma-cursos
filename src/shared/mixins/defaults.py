from django.db import models


class DefaultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class DefaultMixin(models.Model):
    class Meta:
        abstract = True

    objects = DefaultManager()
    even_deleted = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    