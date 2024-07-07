from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.db.models import Q

from .models import Course, ClassViewer, Class
from .forms import ExamQuestionForm

from shared.utils.classes import get_percentage_of_course
from shared.utils.certificate import generate_certificate


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


@login_required
@require_http_methods(["GET"])
def watch_class(request, course_slug, class_slug):
    student = request.user.student
    course = get_object_or_404(Course, slug=course_slug)
    current_class = get_object_or_404(Class, slug=class_slug)

    if current_class.course != course:
        return HttpResponse(400)

    class_views = ClassViewer.objects.filter(
        _class__course=course,
        viewer_object_id=student.id,
        viewer_content_type=student.get_content_type()
    )

    if current_class != course.classes.first() and not class_views.exists():
        return redirect(f'/cursos/{course.slug}/aula/{course.classes.first().slug}')

    available_classes = course.classes.all()[:len(class_views) + 1]
    if current_class not in available_classes:
        next_class = course.classes.all()[len(class_views) - 1]
        if next_class != current_class:
            return redirect(f'/cursos/{course.slug}/aula/{next_class.slug}')

    _, _ = ClassViewer.objects.get_or_create(
        _class=current_class,
        viewer_object_id=student.id,
        viewer_content_type=student.get_content_type()
    )

    return render(request, 'pages/courses/classes/watch.html', {
        'course': course,
        'class': current_class
    })


@login_required
@require_http_methods(["GET", "POST"])
def take_exam(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    exam = course.exam

    if get_percentage_of_course(request.user.student, course) < 80:
        return redirect(f'/cursos/{course.slug}/aula/{course.classes.first().slug}')

    if request.method == 'POST':
        form = ExamQuestionForm(request.POST, course_slug=course.slug, student_name=request.user.student.name)
        if form.is_valid():
            percentage = form.save()

            print(percentage)

            if percentage >= 80:
                generate_certificate(
                    student=request.user.student,
                    instructor=course.instructor,
                    course=course,
                    hours=course.get_hours()
                )
                # return meus_certificados.

            else:
                form.add_error(None, f'Vamos lá, você consegue! Você acertou {percentage}% das questões, precisa acertar no mínimo 80%.')

    else:
        form = ExamQuestionForm(course_slug=course.slug)

    return render(request, 'pages/courses/classes/exam.html', {
        'course': course,
        'exam': exam,
        'form': form
    })
