from django.shortcuts import render
from .forms import SignInForm, SignUpForm

def signin(request):   
  if request.method == "POST":
    form = SignInForm(request.POST)
    if form.is_valid():
      return ""
  else:
    form = SignInForm()
  return render(request, "pages/auth/signin.html", {"form": form})
    
def signup(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      return ""
  else:
    form = SignUpForm()
  return render(request, "pages/auth/signup.html", {"form": form})
    
def logout(request):
  pass