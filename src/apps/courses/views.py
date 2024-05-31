from django.shortcuts import redirect
from .models import Course, Category, Instructor

def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        instructor_id = request.POST.get('instructor')
        is_valid = request.POST.get('valid') == 'on'
        accept_guests = request.POST.get('accept_guests') == 'on'
        category_names = request.POST.get('categories').split(',')

        instructor = Instructor.objects.get(pk=instructor_id)

        course = Course.objects.create(
            title=title,
            instructor=instructor,
            valid=is_valid,
            accept_guests=accept_guests
        )

        for name in category_names:
            name = name.strip()
            category, created = Category.objects.get_or_create(title=name)
            course.categories.add(category)
        
        course.save()
        return redirect('success_view')

    return redirect('error_view')
