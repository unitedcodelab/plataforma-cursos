from django.urls import path
from . import views

urlpatterns = [
  path('sair', views._logout, name='logout'),
  path('cadastro', views.signup, name='signup'),
  path('confirmar-email/<str:token>', views.confirm_email, name="confirm_email"),
  path('entrar', views.signin, name='signin'),
]