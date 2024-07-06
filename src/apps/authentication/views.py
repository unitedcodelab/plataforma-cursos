from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

import apps.authentication.threads as threads
import apps.authentication.forms as forms
import shared.utils.auth as utils


def signin(request):
    if request.method == "POST":
        form = forms.SignInForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            next = request.GET.get('next')
            if next:
                return redirect(next)

            return redirect('/home')

    else:
        form = forms.SignInForm()

    return render(request, "pages/auth/signin.html", {
        "form": form
    })


def signup(request):
    step = int(request.GET.get('step', 1))
    token = request.GET.get('t')
    context = {}

    if request.method == "POST":
        if step == 1:
            form = forms.SignUpStep1Form(request.POST)

            if form.is_valid():
                token = form.save()
                return redirect(f'/autenticacao/cadastro?step={step + 1}&t={token}')

        elif step == 2:
            form = forms.SignUpStep2Form(request.POST, token=token)

            if form.is_valid():
                form.save()
                return redirect(f'/autenticacao/cadastro?step={step + 1}&t={token}')

        elif step == 3:
            form = forms.SignUpStep3Form(request.POST, token=token)

            if form.is_valid():
                form.save()

                threads.SendEmailThread(token).start()

                return render(request, "pages/auth/email-sent.html")

    else:
        if step == 1:
            form = forms.SignUpStep1Form()

        elif step == 2:
            form = forms.SignUpStep2Form(token=token)

        elif step == 3:
            form = forms.SignUpStep3Form(token=token)

    if step == 2:
        student = utils.get_student_by_token(token)
        context['student_name'] = student.name.split(' ')[0]

    return render(request, "pages/auth/signup.html", {
        **context,
        "form": form,
        "step": step,
        "token": token
    })


def confirm_email(request, token):
    student = utils.get_student_by_token(token)
    student.verified = True
    student.save()

    utils.get_github_data(token)
    utils.delete_token(token)

    login(request, student.user, backend='django.contrib.auth.backends.ModelBackend')

    return redirect('/home')


@login_required
def _logout(request):
    logout(request)
    return redirect('/autenticacao/entrar')
