from django.contrib.auth.models import Group
from django.forms import *


class GroupForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del grupo',
                    'class': 'form-control',
                    'name': 'names'
                }
            ),
            'permissions': SelectMultiple(
                attrs={
                    'class': 'form-select custom-select ms',
                    'multiple ': 'multiple',
                    'aria-label': 'Default select example'
                }
            )
        }
        exclude = []
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