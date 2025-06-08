from django.db import models


RATE_CHOICES = [
    ('full', 'Полная'),
    ('0.5', '0,5'),
    ('0.25', '0,25'),
    ('0.75', '0,75'),
]

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    contact = models.CharField(max_length=100, verbose_name='Контактные данные')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отдел')
    rate = models.CharField(max_length=100, choices=RATE_CHOICES, verbose_name='Ставка', default='full')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Сотрудник'
        verbose_name_plural = 'Сотрудники'