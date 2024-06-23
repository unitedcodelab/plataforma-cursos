from django.db import models

from shared.utils.mixin import custom_slugify


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
    

class SlugMixin(models.Model):
    class Meta:
        abstract = True

    
    slug = models.SlugField(
        max_length=255,
        unique=True,
    )


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title, self.__class__)
        super().save(*args, **kwargs)
    