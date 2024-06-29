from django.contrib import admin
from django.urls import path

import apps.courses.views as course_views


urlpatterns = [
    path('search', course_views.search_courses, name='search_courses'),
]
