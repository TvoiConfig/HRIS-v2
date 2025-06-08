from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponse
from .forms import DepartmentForm
from .models import Department


class DepartmentListView(ListView):
    model = Department
    template_name = 'departments.html'
    context_object_name = 'departments'

    def get_queryset(self):
        queryset = Department.objects.all()
        search_query = self.request.GET.get('search', '').strip()
        sort_option = self.request.GET.get('sort', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(desc__icontains=search_query)
            )

        if sort_option == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_option == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort_option == 'created_new':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'created_old':
            queryset = queryset.order_by('created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_query'] = self.request.GET.get('search', '')
        context['sort_option'] = self.request.GET.get('sort', '')
        return context

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('<script>location.reload()</script>')

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('departments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('<script>location.reload()</script>')