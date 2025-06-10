from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class StaffOrDepartmentHeadRequiredMixin(AccessMixin):
    """
    Пускает:
     - любых is_staff пользователей
     - любых аутентифицированных пользователей, у которых user.employee.headed_department != None
    Иначе — редиректит на login_url или на no_permission.
    """
    login_url = 'login'
    no_permission_url = 'login'  # определите в urls.py страницу «Нет доступа»

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # 1) неавторизованных — на логин
        if not user.is_authenticated:
            return redirect(self.login_url)

        # 2) is_staff всегда можно
        if user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # 3) глав отдела: проверяем связанный Employee и headed_department
        try:
            employee = user.employee
        except user.employee.RelatedObjectDoesNotExist:
            return redirect(self.no_permission_url)

        if getattr(employee, 'headed_department', None) is None:
            return redirect(self.no_permission_url)

        # всё ок
        return super().dispatch(request, *args, **kwargs)