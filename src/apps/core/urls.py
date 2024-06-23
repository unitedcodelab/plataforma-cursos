from django.contrib import admin
from django.urls import path

import apps.core.views as core_views


urlpatterns = [
    path('home', core_views.home, name='home'),
]
