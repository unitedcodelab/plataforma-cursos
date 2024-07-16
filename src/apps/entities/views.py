from django.shortcuts import render
from . models import UnitStudent

def user_profile(request):
  if request.method == "GET":
    students = UnitStudent.objects.all()
    context = {
      "students": students
    }
    return render(request, "pages/user_profile.html", context)
    