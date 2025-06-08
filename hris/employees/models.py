from django.db import models
from django.utils import timezone


RATE_CHOICES = [
    ('1', 'Полная'),
    ('0.75', '0,75'),
    ('0.5', '0,5'),
    ('0.25', '0,25'),
]
CATEGORY_CHOICES = [
    ('main', 'Основной персонал'),
    ('seasonal', 'Сезонный'),
    ('partTime', 'Совместитель')
]

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО')
    position = models.CharField(max_length=100, verbose_name='Должность')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    contact = models.CharField(max_length=100, verbose_name='Контактные данные')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отдел')
    rate = models.CharField(max_length=100, choices=RATE_CHOICES, verbose_name='Ставка', default='full')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name='Статус сотрудника', default='main')
    start_date = models.DateField(default=timezone.now, verbose_name='Дата трудоустройства')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата увольнения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Сотрудник'
        verbose_name_plural = 'Сотрудники'