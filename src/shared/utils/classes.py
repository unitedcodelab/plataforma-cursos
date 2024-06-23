from django.db.models import Count, F, Max, ExpressionWrapper, IntegerField, Q, Subquery, OuterRef

from apps.courses.models import Course, Class


def get_last_courses(student, limit):
    return Course.objects.filter(
        classes__classviewer__viewer_content_type=student.get_content_type(),
        classes__classviewer__viewer_object_id=student.id
    ).annotate(
        latest_class_created_at=Max('classes__classviewer__created_at'),
        watched_classes=Count(
            'classes__classviewer', 
            filter=Q(
                classes__classviewer__viewer_content_type=student.get_content_type(),
                classes__classviewer__viewer_object_id=student.id,
                classes__classviewer___class__course=F('id')
            )
        ),
        total_classes=Subquery(
            Class.objects.filter(
                course=OuterRef('pk')
            ).values('course').annotate(
                class_count=Count('id')
            ).values('class_count'),
            output_field=IntegerField()
        ),
        percentage=ExpressionWrapper(
            F('watched_classes') * 100.0 / F('total_classes'),
            output_field=IntegerField()
        )
    ).order_by('-latest_class_created_at')[:limit]
