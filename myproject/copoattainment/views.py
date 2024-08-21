from django.http import JsonResponse
from django.views import View
from .models import Student, COAttainment,Programme
from .utils import calculate_co_attainment
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json

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


@csrf_exempt  # Disables CSRF for this view
def bulk_create_students(request):
    if request.method == 'POST':
        try:
            print(request.body)
            # Parse JSON data from the request body
            body = json.loads(request.body)
            students_data = body.get('students', [])
            print(students_data)

            if not students_data:
                return JsonResponse({"error": "No student data provided"}, status=400)

            # List to hold the Student objects
            student_objects = []

            # Manually validate and prepare each student record
            for student in students_data:
                try:
                    student_id = student['student_id']
                    first_name = student['first_name']
                    last_name = student['last_name']
                    program_id = student['program']  # Assuming program is passed as ID
                    enrollment_year = student['enrollment_year']

                    # Fetch the Program object for the foreign key relationship
                    program = Programme.objects.get(programme_id=program_id)

                    # Create a Student object but don't save it yet
                    student_obj = Student(
                        student_id=student_id,
                        first_name=first_name,
                        last_name=last_name,
                        program=program,
                        enrollment_year=enrollment_year
                    )
                    student_objects.append(student_obj)
                except KeyError as e:
                    # Return error if a required field is missing
                    return JsonResponse({
                        "error": f"Missing field: {str(e)}"
                    }, status=400)
                except Programme.DoesNotExist:
                    return JsonResponse({
                        "error": f"Program with ID {program_id} does not exist"
                    }, status=400)
                except ValueError as e:
                    return JsonResponse({
                        "error": f"Invalid data format: {str(e)}"
                    }, status=400)
            print("stud object",student_objects)
            # Bulk create the valid student objects
            Student.objects.bulk_create(student_objects)

            return JsonResponse({"message": "Students created successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
