from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from employees.models import Employee
from departments.models import Department


def department_head_required(param_name='department_id', login_url='login', no_perm_url='no_permission'):
    """
    Декоратор для вью, где в kwargs есть параметр `department_id`
    указывающий на id отдела. Только его руководитель сможет зайти.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # 1) проверяем аутентификацию
            if not request.user.is_authenticated:
                return redirect(login_url)

            # 2) получаем Employee для текущего пользователя
            try:
                employee = request.user.employee
            except Employee.DoesNotExist:
                return redirect(no_perm_url)

            # 3) получаем Department из URL-параметров
            dept_id = kwargs.get(param_name)
            department = get_object_or_404(Department, id=dept_id)

            # 4) проверяем, что этот employee — руководитель
            if department.head_id != employee.id:
                return redirect(no_perm_url)

            # всё ок, передаём дальше
            return view_func(request, *args, **kwargs)

        return _wrapped
    return decorator
