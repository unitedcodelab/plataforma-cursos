import requests
from random import choices
from string import ascii_letters, digits

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config.settings import APLICATION_URL, EMAIL_HOST_USER
from apps.entities.models import Student
from apps.authentication.models import SignUpToken


def random_string(length: int) -> str:
    return ''.join(choices(ascii_letters + digits, k=length))


def generate_token(student_enroll_number: str):
    tokenModel, created = SignUpToken.objects.get_or_create(student_enroll_number=student_enroll_number)
    
    if created:
        tokenModel.token = random_string(64)
        tokenModel.save()

    return tokenModel


def update_token(token: str):
    tokenModel = SignUpToken.objects.get(token=token)
    tokenModel.token = random_string(64)
    tokenModel.save()
    return tokenModel.token


def delete_token(token: str):
    SignUpToken.objects.get(token=token).delete()


def get_student_by_token(token: str):
    token_model = get_object_or_404(SignUpToken, token=token)
    student = Student.even_not_verified.get(enroll_number=token_model.student_enroll_number)
    return student


def send_email(token: str):
    new_token = update_token(token)
    student = get_student_by_token(new_token)

    send_mail(
        'Confirmação de cadastro',
        f'Olá {student.name}, clique no link para confirmar seu cadastro: {APLICATION_URL}/autenticacao/confirmar-email/{new_token}',
        EMAIL_HOST_USER,
        [student.email],
        fail_silently=False,
    )


def get_github_data(token):
    student = get_student_by_token(token)

    response = requests.get(f"https://api.github.com/users/{student.github}")
    data = response.json()

    student.slug = data['login']
    student.photo = data['avatar_url']
    student.biograph = data['bio']

    student.save()
