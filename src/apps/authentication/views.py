from django.shortcuts import render
from .forms import SignInForm

def signin(request):   
  if request.method == "POST":
    form = SignInForm(request.POST)
    if form.is_valid():
      return ""
  else:
    form = SignInForm()
  return render(request, "pages/auth/signin.html", {"form": form})
    
def signup(request):
  if request.method == 'GET':
    return render(request, 'authentication.html')
    
def logout(request):
  pass