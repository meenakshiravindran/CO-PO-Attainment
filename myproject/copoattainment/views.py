from django.http import JsonResponse
from django.views import View
from .models import Student, COAttainment
from .utils import calculate_co_attainment

class CalculateAttainmentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(student_id=student_id)
        calculate_co_attainment(student.student_id)
        return JsonResponse({'status': 'CO attainment calculated'}, status=200)

class COAttainmentView(View):
    def get(self, request, student_id):
        attainments = COAttainment.objects.filter(student_id=student_id)
        data = list(attainments.values('co_number', 'total_marks_obtained', 'total_marks_possible'))
        return JsonResponse(data, safe=False, status=200)

