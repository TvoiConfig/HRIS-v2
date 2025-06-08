from django.urls import path
from .views import EmployeesListView, EmployeesCreateView

urlpatterns = [
    path('employees/', EmployeesListView.as_view(), name='employees'),
    path('employees/create/', EmployeesCreateView.as_view(), name='employees_create'),
]