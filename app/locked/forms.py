from django import forms
from user.models import User
class ActivateForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Nombre',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Apellidos',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Nombre de usuario',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    date_joined = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Fecha de registro',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Correo eletonico',
            'class': 'form-control',
            'autocomplete': 'off',
            'readonly': True,
            'style': 'cursor: pointer;',
            'required': True
        }
    ))
    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            raise forms.ValidationError('El usuario no existe')
        return cleaned
    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)
class ChangeActivateUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Ingrese su nombre de usuario',
            'class': 'form-control',
            'autocomplete': 'off',
            'autocomplete': 'off'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su nueva contraseña',
            'class': 'form-control',
        }
    ))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repita la contraseña',
            'class': 'form-control',
            'autocomplete': 'off'
        }
    ))
    def clean(self):
        cleaned = super().clean()
        username = cleaned['username']
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            if password != confirmPassword:
                raise forms.ValidationError('Las contraseñas deben coincidir')
        else:
            raise forms.ValidationError('El usuario no existe')
        return cleaned