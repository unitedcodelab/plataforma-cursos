from django.db import models


class SignUpToken(models.Model):
    student_enroll_number = models.CharField(max_length=10)
    token = models.CharField(max_length=64)