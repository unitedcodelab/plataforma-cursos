from django.contrib import admin

from .models import *


class UnitStudentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'enroll_number', 'course', 'campus', 'period', 'enrollment_year')
    list_filter = ('course', 'campus', 'period', 'enrollment_year')


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'enroll_number', 'verified')

    def get_queryset(self, request):
        return self.model.even_not_verified.get_queryset()


admin.site.register(UnitStudent, UnitStudentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
admin.site.register(Guest)
