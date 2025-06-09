from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from employees.models import Employee
from .models import Schedule
from calendar import HTMLCalendar


class BaseScheduleView(View):
    template_name = 'schedule.html'

    def get_calendar_context(self, employee, year=None, month=None):
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


@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class EmployeeScheduleView(BaseScheduleView):
    permission_required = 'employees.view_schedule'
    def get(self, request, employee_id, year=None, month=None):
        employee = get_object_or_404(Employee, pk=employee_id)
        context = self.get_calendar_context(employee, year, month)
        return render(request, self.template_name, context)


class MyScheduleView(LoginRequiredMixin, BaseScheduleView):
    def get(self, request, year=None, month=None):
        if not hasattr(request.user, 'employee'):
            return render(request, 'no_employee.html', status=404)

        employee = request.user.employee
        context = self.get_calendar_context(employee, year, month)
        return render(request, self.template_name, context)