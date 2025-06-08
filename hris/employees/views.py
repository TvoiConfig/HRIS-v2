from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import EmployeeForm
from .models import Employee
from core.utils.query import apply_search_and_sort

class EmployeesListView(ListView):
    model = Employee
    template_name = 'employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '').strip()
        sort_option = self.request.GET.get('sort', '')

        return apply_search_and_sort(
            Employee.objects.all(),
            search_query,
            sort_option,
            search_fields=['name', 'position', 'department__name'],
            sort_mapping={
                'name_asc': 'name',
                'name_desc': '-name',
                'created_new': '-created_at',
                'created_old': 'created_at',
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['sort_option'] = self.request.GET.get('sort', '')
        return context

class EmployeesCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')