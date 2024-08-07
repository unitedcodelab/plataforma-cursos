from django.contrib import admin
from django.urls import path

import apps.courses.views as course_views


urlpatterns = [
    path('search', course_views.search_courses, name='search_courses'),
    path('explorar', course_views.explore_courses, name='explore_courses'),
    path('<slug:course_slug>', course_views.course_detail, name='course_detail'),
    path('<slug:course_slug>/aula/<slug:class_slug>', course_views.watch_class, name='watch_class'),
    path('<slug:course_slug>/prova', course_views.take_exam, name='take_exam'),
]
