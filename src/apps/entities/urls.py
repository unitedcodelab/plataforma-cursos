from django.urls import path

import apps.entities.views as views

urlpatterns = [
  path('', views.user_profile, name='user_profile'),
  path('certificados/', views.user_certificates, name='user_certificates')
]