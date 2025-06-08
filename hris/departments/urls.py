from django.urls import path
from .views import DepartmentListView, DepartmentCreateView, DepartmentDeleteView, DepartmentUpdateView

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='departments'),
    path('departments/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
]