from datetime import datetime
from crum import get_current_request
from django.forms import *
from django import forms
from categories.models import Categories
from income.models import Income
class IncomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        request = get_current_request()
        for form in self.visible_fields():
            # form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['description'].widget.attrs['autofocus'] = True
            self.fields['state'].widget.attrs['class'] = 'form-control'
        # self.fields['categorie'].queryset = Categories.objects.none()
        categorie = Categories.objects.filter(user_id=request.user.id).distinct()
        self.fields['categorie'].queryset = categorie
    class Meta:
        model = Income
        fields = 'description', 'amount', 'date_joined', 'annotations', 'categorie', 'state', 'iva', 'totaliva', 'total', 'image'
        widgets = {
            'description': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Introduzca una breve descripción',
                    'style': 'height:130px; resize:none;',
                },
            ),
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0,0',
                },
            ),
            'iva': NumberInput(
                attrs={
                    'class': 'col-md-8 form-control text-center',
                    'style':'width: 30%; padding-left:8px;',
                    'readonly': 'readonly',
                    'style': 'cursor: pointer',
                },
            ),
            'totaliva': NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly',
                    'value': 0.00,
                    'style': 'cursor: pointer'
                },
            ),
            'total': NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly',
                    'value': 0.00,
                    'style': 'cursor: pointer',
                },
            ),
            'categorie': Select(
              attrs={
                  'class': 'form-control select2'
              }
            ),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'annotations': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese comentarios',
                    'style': 'height:130px; resize:none;'
                }
            ),
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
