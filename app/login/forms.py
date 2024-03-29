from datetime import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from security.choices import LOGIN_TYPE
from security.models import AccessUsers
from user.models import User
class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Ingrese su nombre de usuario',
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
            raise forms.ValidationError('El campo username no puede ser vacío')
        elif len(password) == 0:
            raise forms.ValidationError('El campo password no puede ser vacío')
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            user = queryset[0]
            intent = user.accessusers_set.filter(type=LOGIN_TYPE[1][0], date_joined=datetime.now().date()).count()
            if not user.is_active:
                    raise forms.ValidationError('El usuario ha sido bloqueado. Comuníquese con su administrador por medio del correo electrónico costcontrolsa@gmail.com')
            if authenticate(username=username, password=password) is None:
                AccessUsers(user=user, type=LOGIN_TYPE[1][0]).save()
                if intent > 2:
                    user.is_active = False
                    user.save()
                    raise forms.ValidationError('Su usuario ha sido bloqueado por superar el limite de intentos fallidos')
                count = 3 - intent
                raise forms.ValidationError(f"Usuario o contraseña incorrectos. Le quedan {count} {'intento' if count == 1 else 'intentos'}. Si supera los 3 intentos fallidos su cuenta será bloqueada")
            AccessUsers(user=user).save()
            return cleaned
        raise forms.ValidationError('Usuario o contraseña incorrectos')
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
        user = cleaned['username']
        if not User.objects.filter(username=user).exists():
            raise forms.ValidationError('El usuario no existe')
        u = User.objects.get(username=user)
        if u.is_active != True:
            raise forms.ValidationError('El usuario ha sido bloqueado. Comuníquese con su administrador por medio del correo electrónico costcontrolsa@gmail.com')
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