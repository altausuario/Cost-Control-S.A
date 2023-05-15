from django import forms
from django.contrib.auth.models import Group


from user.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter a username',
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

