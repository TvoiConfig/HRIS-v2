from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import EmployeeForm
from .models import Employee
from core.utils.query import apply_search_and_sort
from core.mixins import StaffOrDepartmentHeadRequiredMixin


class EmployeesListView(StaffOrDepartmentHeadRequiredMixin, ListView):
    model = Employee
    template_name = 'employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        qs = Employee.objects.all()

        user = self.request.user
        # Если не is_staff — фильтрует по отделу главы
        if not user.is_staff:
            # берет отдел, которым он руководит
            dept = user.employee.headed_department
            qs = qs.filter(department=dept)

        # применение поиска и сортировки
        search_query = self.request.GET.get('search', '').strip()
        sort_option = self.request.GET.get('sort', '')

        return apply_search_and_sort(
            qs,
            search_query,
            sort_option,
            search_fields=['name', 'position', 'department__name'],
            sort_mapping={
                'name_asc': 'name',
                'name_desc': '-name',
                'start_date_new': '-start_date',
                'start_date_old': 'start_date',
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_option'] = self.request.GET.get('sort', '')
        return context

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class EmployeesCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class EmployeesUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class EmployeesDeleteView(DeleteView):
    model = Employee
    template_name = 'employees_confirm_delete.html'
    success_url = reverse_lazy('employees')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('<script>location.reload()</script>')
