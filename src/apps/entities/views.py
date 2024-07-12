from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.courses.models import Certificate


def user_profile(request):
    if request.method == "GET":
        return render(request, "pages/profile/user_profile.html")


@require_http_methods(["GET"])
def user_certificates(request):
    certificates = Certificate.objects.filter(
        student_object_id=request.user.student.id,
        student_content_type=request.user.student.get_content_type()
    )
    return render(request, "pages/profile/certificates.html", {
        "certificates": certificates
    })
