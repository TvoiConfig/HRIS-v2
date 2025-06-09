from django.urls import path
from .views import EmployeeScheduleView, MyScheduleView, ToggleScheduleView

urlpatterns = [
    path('schedule/<int:employee_id>/<int:year>/<int:month>/', EmployeeScheduleView.as_view(), name='schedule'),
    path('schedule/<int:employee_id>/', EmployeeScheduleView.as_view(), name='current_schedule'),
    path('my-schedule/', MyScheduleView.as_view(), name='my_schedule'),
    path('my-schedule/<int:year>/<int:month>/', MyScheduleView.as_view(), name='my_schedule_month'),
    path('schedule/toggle/<int:employee_id>/<int:year>/<int:month>/<int:day>/', ToggleScheduleView.as_view(), name='toggle_schedule'),
]