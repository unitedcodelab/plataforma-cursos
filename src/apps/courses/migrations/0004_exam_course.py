# Generated by Django 5.0.6 on 2024-07-05 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_classviewer__class'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='course',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
            preserve_default=False,
        ),
    ]
