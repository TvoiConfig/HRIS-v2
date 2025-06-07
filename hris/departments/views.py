from django.db.models import Q
from django.shortcuts import render
from .models import Department

# Create your views here.
def departments_view(request):
    search_query = request.GET.get('search', '').strip()
    sort_option = request.GET.get('sort', '')

    departments = Department.objects.all()

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(desc__icontains=search_query)
        )

    if sort_option == 'name_asc':
        departments = departments.order_by('name')
    elif sort_option == 'name_desc':
        departments = departments.order_by('-name')
    elif sort_option == 'created_new':
        departments = departments.order_by('-created_at')
    elif sort_option == 'created_old':
        departments = departments.order_by('created_at')

    return render(request, 'departments.html', {
        'departments': departments,
        'search_query': search_query,
        'sort_option': sort_option
    })