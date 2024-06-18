from django.contrib import admin

from .models import *


class UnitStudentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'enroll_number', 'course', 'campus', 'period', 'enrollment_year')
    list_filter = ('course', 'campus', 'period', 'enrollment_year')


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Guest)
admin.site.register(UnitStudent, UnitStudentAdmin)
