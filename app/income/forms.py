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
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['description'].widget.attrs['autofocus'] = True
        categorie = Categories.objects.filter(user_id=request.user.id).distinct()
        self.fields['categorie'].queryset = categorie
        print(usuario)

    class Meta:
        model = Income
        fields = 'description', 'amount', 'date_creation', 'annotations', 'categorie', 'state'
        widgets = {
            'description': Textarea(
                attrs={
                    'placeholder': 'Introduzca una breve descripción',
                    'style': 'height:130px; resize:none;',
                },

            ),
            'amount': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el valor del ingreso',
                },

            ),
            'date_creation': TextInput(
                attrs={
                    'type': 'datetime-local',
                }
            ),
            'annotations': Textarea(
                attrs={
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
