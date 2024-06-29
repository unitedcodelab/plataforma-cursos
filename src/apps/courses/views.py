import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse

from .models import Course


@login_required
@require_http_methods(["GET"])
def search_courses(request):
    query = request.GET.get('q')
    limit = request.GET.get('l', 3)

    if not query or not isinstance(limit, int):
        return HttpResponse(400)

    courses = Course.objects.filter(title__icontains=query).values(
        'id', 'title', 'thumbnail'
    )[:limit]

    if len(courses) > 0:
        return JsonResponse({
            'courses': list(courses)
        })        

    return HttpResponse(404)
