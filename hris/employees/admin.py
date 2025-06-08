from django.contrib import admin

from employees.models import Employee


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'position',)
    list_filter = ('created_at',)
    search_fields = ('name', 'department', 'position',)
    ordering = ('name',)
