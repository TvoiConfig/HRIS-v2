from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название отдела'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание отдела',
                'rows': 3
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Гарантирует, что всем полям будет добавлен form-control
            for field_name in self.fields:
                field = self.fields[field_name]

                # Убирает стандартные подсказки
                field.help_text = None

                # Добавляет form-control если его еще нет
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

                # Для текстовых полей добавляет placeholder
                if isinstance(field.widget, forms.TextInput) and not field.widget.attrs.get('placeholder'):
                    field.widget.attrs['placeholder'] = f'Введите {field.label.lower()}'