from django.db import models
from django.contrib.auth.models import User

class PersonMixin(models.Model):
    class Meta:
        abstract = True

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
