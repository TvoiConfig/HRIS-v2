from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user',
            'name',
            'department',
            'position',
            'date_of_birth',
            'contact',
            'rate',
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'date_of_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            # Для всех полей (кроме чекбоксов) добавляет form-control
            if self.fields[field].widget.input_type != 'checkbox':
                self.fields[field].widget.attrs.update({'class': 'form-control'})