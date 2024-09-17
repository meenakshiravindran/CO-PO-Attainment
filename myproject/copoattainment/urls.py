from django.urls import path
from . import views
from .views import CalculateAttainmentView, COAttainmentView,custom_login_view,get_students_by_programme_name_and_year,get_programmes_and_enrollment_years,create_programme,create_assessment_pattern,create_question_pattern,create_course

urlpatterns = [
    path('api/students/bulk_create/', views.bulk_create_students, name='bulk_create_students'),
    path('students/<str:student_id>/calculate/', CalculateAttainmentView.as_view(), name='calculate_attainment'),
    path('students/<str:student_id>/attainments/', COAttainmentView.as_view(), name='co_attainment'),
    path('api/login/', custom_login_view, name='login'),
    path('api/students/', get_students_by_programme_name_and_year, name='get_students_by_programme_name_and_year'),
    path('api/programmes-enrollment/', get_programmes_and_enrollment_years, name='programmes_enrollment'),
    path('create-programme/', create_programme, name='create_programme'),
    path('create-course/', create_course, name='create_course'),
    path('create-assessment-pattern/', create_assessment_pattern, name='create_assessment_pattern'),
    path('create-question-pattern/', create_question_pattern, name='create_question_pattern'),
]
