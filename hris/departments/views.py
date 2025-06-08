from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import render
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
