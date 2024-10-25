from django.http import JsonResponse
from django.views import View
from .models import Student, COAttainment, Programme,AssessmentPattern,Course,QuestionPattern
from django.conf import settings
from django.contrib.auth import authenticate
from .utils import calculate_co_attainment
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import jwt
import json
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class CalculateAttainmentView(View):
    def get(self, request, student_id):
        student = Student.objects.get(student_id=student_id)
        calculate_co_attainment(student.student_id)
        return JsonResponse({"status": "CO attainment calculated"}, status=200)


class COAttainmentView(View):
    def get(self, request, student_id):
        attainments = COAttainment.objects.filter(student_id=student_id)
        data = list(
            attainments.values(
                "co_number", "total_marks_obtained", "total_marks_possible"
            )
        )
        return JsonResponse(data, safe=False, status=200)


@csrf_exempt  # Disables CSRF for this view
def bulk_create_students(request):
    if request.method == "POST":
        try:
            print(request.body)
            # Parse JSON data from the request body
            body = json.loads(request.body)
            students_data = body.get("students", [])
            print(students_data)

            if not students_data:
                return JsonResponse({"error": "No student data provided"}, status=400)

            # List to hold the Student objects
            student_objects = []

            # Manually validate and prepare each student record
            for student in students_data:
                try:
                    student_id = student["student_id"]
                    first_name = student["first_name"]
                    last_name = student["last_name"]
                    program_id = student["program"]  # Assuming program is passed as ID
                    enrollment_year = student["enrollment_year"]

                    # Fetch the Program object for the foreign key relationship
                    program = Programme.objects.get(programme_id=program_id)

                    # Create a Student object but don't save it yet
                    student_obj = Student(
                        student_id=student_id,
                        first_name=first_name,
                        last_name=last_name,
                        program=program,
                        enrollment_year=enrollment_year,
                    )
                    student_objects.append(student_obj)
                except KeyError as e:
                    # Return error if a required field is missing
                    return JsonResponse(
                        {"error": f"Missing field: {str(e)}"}, status=400
                    )
                except Programme.DoesNotExist:
                    return JsonResponse(
                        {"error": f"Program with ID {program_id} does not exist"},
                        status=400,
                    )
                except ValueError as e:
                    return JsonResponse(
                        {"error": f"Invalid data format: {str(e)}"}, status=400
                    )
            print("stud object", student_objects)
            # Bulk create the valid student objects
            Student.objects.bulk_create(student_objects)

            return JsonResponse(
                {"message": "Students created successfully"}, status=201
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def custom_login_view(request):
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body.decode("utf-8"))
            email = data.get("email")
            password = data.get("password")

            # Authenticate the user by email
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    # Generate a JWT token
                    token = jwt.encode(
                        {"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256"
                    )
                    return JsonResponse({"token": token}, status=200)
                else:
                    return JsonResponse({"error": "Invalid credentials"}, status=400)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_students_by_programme_name_and_year(request):
    if request.method == 'GET':
        try:
            # Extract parameters from the request
            programme_name = request.GET.get('programme_name')
            enrollment_year = request.GET.get('enrollment_year')
            
            # Validate parameters
            if not programme_name or not enrollment_year:
                return JsonResponse({'error': 'Missing parameters'}, status=400)
            
            # Fetch the Programme object by name
            try:
                program = Programme.objects.get(name=programme_name)
            except Programme.DoesNotExist:
                return JsonResponse({'error': f'Program with name "{programme_name}" does not exist'}, status=400)
            
            # Fetch students based on programme and enrollment year
            students = Student.objects.filter(program=program, enrollment_year=enrollment_year)
            student_data = list(students.values('student_id', 'first_name', 'last_name', 'program', 'enrollment_year'))
            
            return JsonResponse(student_data, safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_programmes_and_enrollment_years(request):
    if request.method == 'GET':
        try:
            # Fetch all programmes
            programmes = Programme.objects.values_list('name', flat=True)
            
            # Fetch distinct enrollment years from the Student model
            enrollment_years = Student.objects.values_list('enrollment_year', flat=True).distinct()
            assessment_patterns = AssessmentPattern.objects.values('assessment_type','course')
            courses = Course.objects.values('course_id','name')
            # Prepare the response data
            response_data = {
                'programmes': list(programmes),
                'enrollment_years': list(enrollment_years),
                'courses': list(courses),
                'assessment_patterns': list(assessment_patterns)
            }
            
            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def create_programme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            programme_id = data.get('programme_id')
            name = data.get('name')

            if not programme_id or not name:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            programme = Programme(programme_id=programme_id, name=name)
            programme.save()

            return JsonResponse({'message': 'Programme created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            name = data.get('name')
            credits = data.get('credits')
            programme = data.get('programme')

            if not course_id or not name or not credits or not programme:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            try:
                programme = Programme.objects.get(name=programme)
            except Programme.DoesNotExist:
                return JsonResponse({'error': 'Programme not found'}, status=400)

            course = Course(course_id=course_id, name=name, credits=credits, programme=programme)
            course.save()

            return JsonResponse({'message': 'Course created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_assessment_pattern(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course = data.get('course')
            assessment_type = data.get('assessment_type')
            total_marks = data.get('total_marks')

            if not course or not assessment_type or not total_marks:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            try:
                course = Course.objects.get(name=course)
            except Course.DoesNotExist:
                return JsonResponse({'error': 'Course not found'}, status=400)

            assessment_pattern = AssessmentPattern(course=course, assessment_type=assessment_type, total_marks=total_marks)
            assessment_pattern.save()

            return JsonResponse({'message': 'Assessment Pattern created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_question_pattern(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            assessment_pattern_id = data.get('assessment_pattern')
            question_type = data.get('question_type')
            total_questions = data.get('total_questions')
            questions_to_answer = data.get('questions_to_answer')
            marks_per_question = data.get('marks_per_question')

            if not assessment_pattern_id or not question_type or not total_questions or not questions_to_answer or not marks_per_question:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            try:
                assessment_pattern = AssessmentPattern.objects.get(id=assessment_pattern_id)
            except AssessmentPattern.DoesNotExist:
                return JsonResponse({'error': 'Assessment Pattern not found'}, status=400)

            question_pattern = QuestionPattern(
                assessment_pattern=assessment_pattern,
                question_type=question_type,
                total_questions=total_questions,
                questions_to_answer=questions_to_answer,
                marks_per_question=marks_per_question
            )
            question_pattern.save()

            return JsonResponse({'message': 'Question Pattern created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_programmes(request):
    if request.method == 'GET':
        programmes = Programme.objects.all()
        programme_list = [{'id': programme.programme_id, 'name': programme.name} for programme in programmes]
        return JsonResponse(programme_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def get_assessment_patterns(request):
    patterns = AssessmentPattern.objects.all().values('id', 'name') 
    return JsonResponse(list(patterns), safe=False)