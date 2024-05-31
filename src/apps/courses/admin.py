from django.contrib import admin

from .models import *


admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Category)

admin.site.register(Class)
admin.site.register(ClassViewer)

admin.site.register(Exam)
admin.site.register(ExamViewer)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuestionViewer)
