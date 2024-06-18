from django.contrib import admin

from .models import *

class UnitStudentAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Guest)
admin.site.register(UnitStudent, UnitStudentAdmin)
