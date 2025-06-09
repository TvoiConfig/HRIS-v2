from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import DepartmentForm
from .models import Department
from core.utils.query import apply_search_and_sort

class DepartmentListView(ListView):
    model = Department
    template_name = 'departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '').strip()
        sort_option = self.request.GET.get('sort', '').strip()

        return apply_search_and_sort(
            Department.objects.all(),
            search_query,
            sort_option,
            search_fields=['name', 'desc'],
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

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

@method_decorator(staff_member_required(login_url='login'), name='dispatch')
class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('departments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('<script>location.reload()</script>')