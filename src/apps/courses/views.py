from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from .models import Course, ClassViewer


@login_required
@require_http_methods(["GET"])
def search_courses(request):
    query = request.GET.get('q')
    limit = request.GET.get('l', 3)

    if not query or not isinstance(limit, int):
        return HttpResponse(400)

    courses = get_list_or_404(Course, title__icontains=query).values(
        'id', 'title', 'thumbnail'
    )[:limit]
    
    return JsonResponse({
        'courses': list(courses)
    })        


@login_required
@require_http_methods(["GET"])
def explore_courses(request):
    courses = Course.objects.filter(
        ~Q(classes__viewers__viewer_object_id=request.user.student.id)
    ).annotate(
        categories_list=ArrayAgg('categories__title')
    )

    return render(request, 'pages/courses/explore.html', {
        'courses': courses
    })


@login_required
@require_http_methods(["GET"])
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    
    course.total_students = ClassViewer.objects.filter(
        _class__in=course.classes.all()
    ).distinct('viewer_object_id').count()

    return render(request, 'pages/courses/detail.html', {
        'course': course
    })
