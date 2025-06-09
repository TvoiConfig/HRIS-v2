from django.db import models
from employees.models import Employee

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время конца")

    class Meta:
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"
        unique_together = ('employee', 'date')

    def __str__(self):
        return f'{self.employee} - {self.date}'