from django.urls import path
from .views import EmployeesListView, EmployeesCreateView, EmployeesUpdateView, EmployeesDeleteView

urlpatterns = [
    path('employees/', EmployeesListView.as_view(), name='employees'),
    path('employees/create/', EmployeesCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/edit/', EmployeesUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeesDeleteView.as_view(), name='employee_delete'),
]