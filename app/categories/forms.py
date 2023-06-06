from crum import get_current_request
from django.forms import *
from categories.models import Categories
class CategoriesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['name'].widget.attrs['autofocus'] = True
    class Meta:
        model = Categories
        fields = 'name', 'description',
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                },
            ),
            'description': Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripcion',
                    'style': 'height:130px; resize:none;',
                },
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
