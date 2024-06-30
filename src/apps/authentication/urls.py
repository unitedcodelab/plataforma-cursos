from django.urls import path
from . import views

urlpatterns = [
  path('sair', views.logout, name='logout'),
  path('cadastro', views.signup, name='signup'),
  path('entrar', views.signin, name='signin'),
]