from django.contrib import admin

from .models import *



class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name', 'created_at')

    def course_name(self, obj):
        return obj.course.title


class ClassViewerAdmin(admin.ModelAdmin):
    list_display = ('viewer_name', 'class_title', 'created_at')

    def viewer_name(self, obj):
        return obj.viewer.name

    def class_title(self, obj):
        return obj._class.title


admin.site.register(Instructor)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category)

admin.site.register(Class, ClassAdmin)
admin.site.register(ClassViewer, ClassViewerAdmin)

admin.site.register(Exam)
admin.site.register(ExamViewer)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuestionViewer)
