from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

from apps.entities.models import Student

import shared.utils.classes as classes_utils


@require_http_methods(["GET"])
def index(request):
    return render(request, 'pages/index.html')


@login_required
@require_http_methods(["GET"])
def home(request):
    last_courses = classes_utils.get_last_courses(request.user.student, limit=3)

    return render(request, 'pages/home.html', {
        'last_courses': last_courses
    })
