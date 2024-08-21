from django.urls import path
from . import views
from .views import CalculateAttainmentView, COAttainmentView

urlpatterns = [
    path('api/students/bulk_create/', views.bulk_create_students, name='bulk_create_students'),
    path('students/<str:student_id>/calculate/', CalculateAttainmentView.as_view(), name='calculate_attainment'),
    path('students/<str:student_id>/attainments/', COAttainmentView.as_view(), name='co_attainment'),
]
