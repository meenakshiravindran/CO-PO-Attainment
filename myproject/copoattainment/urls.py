from django.urls import path
from .views import CalculateAttainmentView, COAttainmentView

urlpatterns = [
    path('students/<str:student_id>/calculate/', CalculateAttainmentView.as_view(), name='calculate_attainment'),
    path('students/<str:student_id>/attainments/', COAttainmentView.as_view(), name='co_attainment'),
]
