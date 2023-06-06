from django.contrib.auth.models import Group
from django.forms import *
from user.models import User
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['first_name'].widget.attrs['autofocus'] = True
    class Meta:
        model = User
        fields = 'groups', 'first_name', 'last_name', 'email', 'username', 'password', 'image',  'is_superuser'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                   'required':''
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese sus email',
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese se nombre de usuario',
                    'class': 'form-control'
                }
            ),
            'password': PasswordInput(
                render_value=True,
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                    'class': 'form-control'
                }
            ),
            'groups': SelectMultiple(
                attrs={
                    'class': 'form-select custom-select ms',
                    'multiple ': 'multiple',
                    'aria-label': 'Default select example'
                }
            ),
            'image': FileInput(
                attrs={
                    'class': 'custom-file-input',
                    'id': 'customFile'
                }
            )
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_active', 'is_staff']
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u =form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['first_name'].widget.attrs['autofocus'] = True
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese sus email',
                    'class': 'form-control'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese se nombre de usuario',
                    'class': 'form-control'
                }
            ),
            'password': PasswordInput(
                render_value=True,
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                    'class': 'form-control'
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups']
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u =form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
class NewUserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
            self.fields['first_name'].widget.attrs['autofocus'] = True
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre',
                    'class': 'form-control text-capitalize',
                   'required':''
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control text-capitalize',
                    'required': ''
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Ingrese su correo eletronico',
                    'class': 'form-control',
                    'required': ''
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre de usuario',
                    'class': 'form-control'
                }
            ),
            'password': PasswordInput(
                render_value=True,
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                    'class': 'form-control'
                }
            ),
            'image': FileInput(
                # render_value=True,
                attrs={
                    'class': 'custom-file-input',
                    'id': 'customFile'
                }
            )
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser']
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u =form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                group = Group.objects.get(name='Usuario')
                u.groups.add(group)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data