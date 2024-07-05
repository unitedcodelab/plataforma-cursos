from django import template

from apps.courses.models import ClassViewer, Course
from apps.entities.models import Student
from shared.utils.classes import get_percentage_of_course

register = template.Library()


@register.filter
def class_status(student_id, class_id) -> str:
    class_views = ClassViewer.objects.filter(
        viewer_object_id=student_id
    )

    if class_views.last()._class.id == class_id:
        return 'watching'

    if class_views.filter(_class_id=class_id).exists():
        return 'watched'

    next_class = class_views.first()._class.course.classes.all()[len(class_views)]
    if next_class.id == class_id:
        return 'next'

    return 'not-watched'


@register.filter
def is_test_available(student, course) -> bool:
    return get_percentage_of_course(student, course) >= 80
