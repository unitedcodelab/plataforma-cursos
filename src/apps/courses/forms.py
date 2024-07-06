from math import ceil

from django import forms
from django.core.exceptions import ValidationError

from apps.entities.models import Student
from .models import Question, OptionViewer, Option, Exam, ExamViewer


class ExamQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        course_slug = kwargs.pop('course_slug')
        student_name = kwargs.pop('student_name', None)
        questions = Question.objects.filter(exam__course__slug=course_slug)

        super().__init__(*args, **kwargs)
        self.course_slug = course_slug
        self.student_name = student_name
        self.questions = questions

        for question in questions:
            options = Option.objects.filter(question=question)
            for _ in options:
                field_name = f'question_{question.id}'
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=[(o.id, o.text) for o in options],
                    widget=forms.RadioSelect
                )

    def clean(self):
        cleaned_data = super().clean()

        for name, value in cleaned_data.items():
            if name.startswith('question_'):
                if not value:
                    raise ValidationError('Todas as perguntas devem ser respondidas.')

        return cleaned_data

    def save(self, commit=True):
        student = Student.objects.get(name=self.student_name)
        exam = Exam.objects.get(course__slug=self.course_slug)
        tries = []

        try_exam = ExamViewer.objects.get_or_create(
            exam=exam,
            viewer_object_id=student.id,
            viewer_content_type=student.get_content_type()
        )
        tries.append(try_exam)

        for answer in self.cleaned_data:
            option = Option.objects.get(id=self.cleaned_data[answer])

            try_answer = OptionViewer.objects.create(
                option=option,
                viewer_object_id=student.id,
                viewer_content_type=student.get_content_type()
            )
            tries.append(try_answer)

        answers_num = len(self.questions) if self.questions else 1
        right_answers = OptionViewer.objects.filter(
            viewer_object_id=student.id,
            viewer_content_type=student.get_content_type(),
            option__question__in=self.questions,
            option__correct=True
        ).count()

        percentage = ceil((right_answers / answers_num) * 100)

        if percentage < 80:
            for t in tries:
                t.delete()

        return percentage
