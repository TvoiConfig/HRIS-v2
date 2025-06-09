from django.db import models


# Create your models here.
class Department(models.Model):
    head = models.OneToOneField(
        'employees.Employee',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='headed_department',
        related_query_name='headed_department',
        verbose_name='Руководитель отдела'
    )
    name = models.CharField(max_length=100, verbose_name='Название отдела')
    desc = models.TextField(verbose_name='Описание отдела')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания отдела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Отдел'
        verbose_name_plural = "Отделы"