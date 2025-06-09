from calendar import HTMLCalendar
from django.utils import timezone
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import StaffOrDepartmentHeadRequiredMixin
from employees.models import Employee
from .models import Schedule
from datetime import date, time
from django.urls import reverse


class BaseScheduleView(View):
    template_name = 'schedule.html'

    @staticmethod
    def get_calendar_context(employee, year=None, month=None):
        today = timezone.now().date()

        # Определяем текущий месяц и год
        year = int(year) if year else today.year
        month = int(month) if month else today.month

        # Рассчитываем предыдущий и следующий месяц
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        # Получаем смены сотрудника за месяц
        shifts = Schedule.objects.filter(
            employee=employee,
            date__year=year,
            date__month=month
        ).only('date', 'start_time', 'end_time')

        # Создаем календарь
        cal = HTMLCalendar(firstweekday=0)
        month_days = cal.monthdayscalendar(year, month)

        # Форматируем данные для шаблона
        weeks = []
        shift_dates = {shift.date.day: shift for shift in shifts}

        for week in month_days:
            week_days = []
            for day in week:
                day_data = {'day': day, 'shift': None}
                if day != 0 and day in shift_dates:
                    shift = shift_dates[day]
                    day_data['shift'] = {
                        'start': shift.start_time.strftime('%H:%M'),
                        'end': shift.end_time.strftime('%H:%M')
                    }
                week_days.append(day_data)
            weeks.append(week_days)

        return {
            'employee': employee,
            'year': year,
            'month': month,
            'month_name': today.replace(year=year, month=month, day=1).strftime('%B'),
            'weeks': weeks,
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'today': today
        }

class EmployeeScheduleView(StaffOrDepartmentHeadRequiredMixin, BaseScheduleView):
    permission_required = 'employees.view_schedule'
    def get(self, request, employee_id, year=None, month=None):
        employee = get_object_or_404(Employee, pk=employee_id)
        context = self.get_calendar_context(employee, year, month)
        return render(request, self.template_name, context)

class MyScheduleView(LoginRequiredMixin, BaseScheduleView):
    login_url = 'login'
    def get(self, request, year=None, month=None):
        if not hasattr(request.user, 'employee'):
            return render(request, 'no_employee.html', status=404)

        employee = request.user.employee
        context = self.get_calendar_context(employee, year, month)
        return render(request, self.template_name, context)

class ToggleScheduleView(StaffOrDepartmentHeadRequiredMixin, BaseScheduleView):
    """
    GET /schedule/toggle/<employee_id>/<year>/<month>/<day>/
    - если есть Schedule → удаляем
    - если нет → создаём с 09:00–18:00
    Перенаправляем обратно на календарь того же сотрудника/месяца.
    """
    def get(self, request, employee_id, year, month, day):
        # достаём сотрудника
        employee = get_object_or_404(Employee, pk=employee_id)

        # составляем дату
        target_date = date(int(year), int(month), int(day))

        # переключаем запись
        obj, created = Schedule.objects.get_or_create(
            employee=employee,
            date=target_date,
            defaults={'start_time': time(9, 0), 'end_time': time(18, 0)}
        )
        if not created:
            # если запись уже была — удаляем
            obj.delete()

        # решаем, куда редиректить: на чужой календарь или на “моё расписание”
        if hasattr(request.user, 'employee') and request.user.employee.id == employee.id:
            # это мой график
            return redirect(
                reverse('my_schedule_month', args=[year, month])
            )

        # чужой график
        return redirect(
            reverse('schedule', args=[employee_id, year, month])
        )