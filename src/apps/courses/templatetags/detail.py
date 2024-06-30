from django import template

from apps.courses.models import ClassViewer

register = template.Library()


@register.filter
def already_subscribed(student_id, course_classes):
    return ClassViewer.objects.filter(
        viewer_object_id=student_id,
        _class__in=course_classes
    ).exists()