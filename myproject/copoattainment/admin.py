from django.contrib import admin
from .models import Student, Programme, Course, AssessmentPattern, QuestionPattern, QuestionCO, StudentAnswer, COAttainment

admin.site.register(Student)
admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(AssessmentPattern)
admin.site.register(QuestionPattern)
admin.site.register(QuestionCO)
admin.site.register(StudentAnswer)
admin.site.register(COAttainment)

