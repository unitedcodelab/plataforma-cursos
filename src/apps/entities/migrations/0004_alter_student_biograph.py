# Generated by Django 5.0.6 on 2024-07-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_student_unit_alter_student_github_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='biograph',
            field=models.TextField(blank=True, null=True),
        ),
    ]
