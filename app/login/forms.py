from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group


from user.models import User

class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Ingerse su nombre de usuario',
            'class': 'form-control',
            'autocomplete': 'off',
            'autofocus': True
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su contraseña',
            'class': 'form-control',
            'autocomplete': 'off'
        }
    ))
    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '')
        password = cleaned.get('password', '')
        if len(username) == 0:
            raise forms.ValidationError('El campo username no puede ser vacio')
        elif len(password) == 0:
            raise forms.ValidationError('El campo password no puede ser vacio')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Usuario o contraseña incorretos')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)





class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Introduzca un nombre de usuario',
            'class': 'form-control',
            'autocomplete': 'off',
            'autofocus': True
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
class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Ingrese su nueva contraseña',
            'class': 'form-control',
            'autocomplete': 'off'
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
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            raise forms.ValidationError('Las contraseñas deben coincidir')
        return cleaned

