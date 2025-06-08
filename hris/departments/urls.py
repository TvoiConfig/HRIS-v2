from django.urls import path
from .views import DepartmentListView

urlpatterns = (
    path('departments/', DepartmentListView.as_view(), name='departments'),
    # path('departments/<int:pk>/edit/', departments_view, name='edit_department'),
    # path('departments/<int:pk>/delete/', departments_view, name='delete_department'),
    # path('departments/add/', departments_view, name='add_department'),
)