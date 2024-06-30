from django.contrib import admin
from django.urls import path

import apps.courses.views as course_views


urlpatterns = [
    path('search', course_views.search_courses, name='search_courses'),
    path('explorar', course_views.explore_courses, name='explore_courses'),
    path('<slug:course_slug>', course_views.course_detail, name='course_detail'),
]
