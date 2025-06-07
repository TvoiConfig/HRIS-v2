from django.shortcuts import render
from .models import Department

# Create your views here.
def departments_view(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})