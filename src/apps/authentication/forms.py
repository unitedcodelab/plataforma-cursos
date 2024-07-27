import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

from apps.entities.extra_models.unit.students import UnitStudent
from apps.entities.models import Student
from shared.utils.auth import generate_token, get_student_by_token


INPUT_FORM_STYLE = "w-full py-2 px-4 border-2 border-blue-gradient border-blue-600 rounded-md text-gray-700 focus:outline-none"


class SignInForm(forms.Form):
    login = forms.CharField(label="Digite seu Email ou Matricula", widget=forms.TextInput(
        attrs={'placeholder': 'Login', 'class': INPUT_FORM_STYLE}
    ))
    password = forms.CharField(label="Digite sua Senha", widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha', 'class': INPUT_FORM_STYLE}
    ))

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if not login or not password:
            raise ValidationError('Por favor, preencha todos os campos.')

        if not authenticate(username=login, password=password):
            raise ValidationError(['Usuário ou senha inválidos.', 'Lembre-se que nossa senha é um pouco mais chatinha ;)'])

        return cleaned_data

    def save(self):
        return authenticate(
            username=self.cleaned_data.get('login'),
            password=self.cleaned_data.get('password')
        )


class SignUpStep1Form(forms.Form):
    enroll_number = forms.CharField(label='Digite sua matrícula', max_length=10, widget=forms.TextInput(
        attrs={'placeholder': 'Matrícula', 'class': INPUT_FORM_STYLE}
    ))

    def clean(self):
        cleaned_data = super().clean()
        enroll_number = cleaned_data.get('enroll_number')

        if not enroll_number:
            raise ValidationError('Por favor, preencha todos os campos.')

        if not UnitStudent.objects.filter(enroll_number=enroll_number).exists():
            raise ValidationError('Matrícula não encontrada.')

        if User.objects.filter(username=enroll_number).exists():
            raise forms.ValidationError('Já Existe um Cadastro com essa Matrícula.')

        if Student.objects.filter(enroll_number=enroll_number).exists():
            raise forms.ValidationError('Já Existe um Cadastro com essa Matrícula.')

        return cleaned_data

    def save(self):
        enroll_number = self.cleaned_data.get('enroll_number')

        unit_student = UnitStudent.objects.get(enroll_number=enroll_number)
        default_user = User.objects.create(username=enroll_number, )

        default_user.set_unusable_password()
        default_user.save()

        student = Student.objects.create(
            user=default_user,
            name=unit_student.name,
            email=unit_student.email,
            enroll_number=enroll_number,
            unit=unit_student,
        )

        student.save()

        token = generate_token(enroll_number).token
        return token


class SignUpStep2Form(forms.Form):
    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token')
        super().__init__(*args, **kwargs)
        self.token = token

    souunit_email = forms.EmailField(label='Digite seu E-mail SouUnit', max_length=100, widget=forms.EmailInput(
        attrs={'placeholder': 'E-mail SouUnit', 'class': INPUT_FORM_STYLE}
    ))

    password = forms.CharField(label='Digite sua Senha', widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha', 'class': INPUT_FORM_STYLE}
    ))

    password_confirm = forms.CharField(label='Confirme sua Senha', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirmação de senha', 'class': INPUT_FORM_STYLE}
    ))

    def clean(self):
        cleaned_data = super().clean()
        souunit_email = cleaned_data.get('souunit_email')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not souunit_email or not password or not password_confirm:
            raise ValidationError('Por favor, preencha todos os campos.')

        if password != password_confirm:
            raise ValidationError('As senhas não conferem.')

        souunit_email_regex = r'^[a-zA-Z0-9._%+-]+@souunit.com.br$'
        if not re.match(souunit_email_regex, souunit_email):
            raise ValidationError('O e-mail deve ser do domínio @souunit.com.br')

        password_regex = (
            ('A senha deve conter no mínimo 12 caracteres', r'^.{12,}$'),
            ('A senha deve conter no mínimo 2 letras maiúsculas', r'^(.*[A-Z]){2,}.*$'),
            ('A senha deve conter no mínimo 2 letras minúsculas', r'^(.*[a-z]){2,}.*$'),
            ('A senha deve conter no mínimo 2 números', r'^(.*\d){2,}.*$'),
            ('A senha deve conter no mínimo 2 caracteres especiais', r'^(.*[^a-zA-Z0-9]){2,}.*$'),
        )

        for error_message, regex in password_regex:
            if not re.match(regex, password):
                raise ValidationError(error_message)

        return cleaned_data

    def save(self):
        student = get_student_by_token(self.token)

        student.email = self.cleaned_data.get('souunit_email')

        student_user = student.user
        student_user.email = self.cleaned_data.get('souunit_email')
        student_user.set_password(self.cleaned_data.get('password'))

        student_user.save()
        student.save()

        return student


class SignUpStep3Form(forms.Form):
    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token')
        super().__init__(*args, **kwargs)
        self.token = token

    github = forms.CharField(label='Digite o seu GitHub', max_length=255, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'GitHub', 'id': 'githubUsername', 'class': INPUT_FORM_STYLE}
    ))

    def save(self):
        student = get_student_by_token(self.token)

        student.github = self.cleaned_data.get('github')
        student.save()

        return student
