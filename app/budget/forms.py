from django.forms import *
from budget.models import Budget
class PresupuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus']= True
    class Meta:
        model = Budget
        fields = 'name', 'total_income', 'total_expenses', 'total'
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'total_income': TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
            'total_expenses': TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
            'total': TextInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
        }