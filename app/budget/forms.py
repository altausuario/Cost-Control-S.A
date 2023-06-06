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
            'total_income': NumberInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
            'total_expenses': NumberInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
            'total': NumberInput(attrs={
                'class': 'form-control',
                'disabled': '',
                'style': 'cursor: pointer;',
                'value': '0.00'
            }),
        }