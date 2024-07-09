from django.shortcuts import render

def user_profile(request):
  if request.method == "GET":
    return render(request, "pages/user_profile.html")