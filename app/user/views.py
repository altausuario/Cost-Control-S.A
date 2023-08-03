from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from group.forms import GroupForm
from user.forms import *
from user.mixins import ValidatePermissionRequiredMinxin
from user.models import User


# Create your views here.
class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
          action = request.POST['action']
          if action == 'searchdata':
              data = []
              position = 1
              for i in User.objects.all().order_by('id'):
                  if i.username != 'altausuario':
                      item = i.toJSON()
                      item['position'] = position
                      data.append(item)
                      position += 1
          elif action == 'block_user':
              data = {}
              try:
                  pkadmin = request.user.id
                  admin = User.objects.get(pk=pkadmin)
                  if admin.has_perm('delete_user') or admin.is_superuser:
                    pk = request.POST['pk']
                    user = User.objects.get(pk=pk)
                    if user.is_active:
                        user.is_active = False
                        user.save()
                        data = {
                            'url':reverse_lazy('usuarios'),
                            'text': f'El usuario {user.first_name} {user.last_name} fue bloqueado exitosamente',
                            'icon': 'success'
                        }
                    else:
                        data = {
                            'url': '',
                            'text': f'El usuario {user.first_name} {user.last_name} ya esta bloqueado',
                            'icon': 'info'
                        }
                  else:
                      data = {
                          'url': reverse_lazy('usuarios'),
                          'text': f'El usuario {admin.first_name} {admin.last_name} no tiene los permisos suficientes para realizar esta acción',
                          'icon': 'error'
                      }
              except Exception as e:
                  data['error'] = str(e)

          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de usuarios'
        context['icon'] = 'fa-list'
        context['url_link'] = reverse_lazy('usuarios')
        context['create_url'] = reverse_lazy('addUsuarios')
        return context
class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('usuarios')
    permission_required = 'add_user'
    url_redirect = reverse_lazy('usuarios')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            elif action == 'new_group':
                with transaction.atomic():
                    formGroup = GroupForm(request.POST)
                    data = formGroup.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo usuario'
        context['action'] = 'add'
        context['icon'] = 'fa-user-plus'
        context['img'] = 'user.png'
        context['url_link'] = self.success_url
        context['formGruop'] = GroupForm
        context['group'] = Group.objects.all().order_by('-id')[:1]
        return context
class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('usuarios')
    permission_required = 'change_user'
    url_redirect = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = User.objects.get(pk=self.object.id)
        if usuario.username == 'altausuario' and usuario.is_superuser:
            return HttpResponseRedirect(reverse_lazy('usuarios'))
        return super().dispatch(request, *args, **kwargs)
    def image_user(self, pk):
        user = User.objects.get(pk=pk)
        if not user.image:
            return 'user.png'
        return user.image
    def user_superuser(self,pk):
        user = User.objects.get(pk=pk)
        return user.is_superuser
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            elif action == 'new_group':
                with transaction.atomic():
                    formGroup = GroupForm(request.POST)
                    data = formGroup.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        context['title'] = 'Editar usuario'
        context['action'] = 'edit'
        context['icon'] = 'fa-user-edit'
        context['img'] = self.image_user(pk)
        context['superuser'] = self.user_superuser(pk)
        context['url_link'] = self.success_url
        context['formGruop'] = GroupForm
        return context
class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('usuarios')
    permission_required = 'delete_user'
    url_redirect = reverse_lazy('usuarios')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = kwargs.get('pk')
        self.get_user_last_login(pk)
        usuario = User.objects.get(pk=self.object.id)
        if usuario.username == 'altausuario' and usuario.is_superuser:
            return HttpResponseRedirect(reverse_lazy('usuarios'))
        return super().dispatch(request, *args, **kwargs)
    def get_user_last_login(self, pk):
        user = User.objects.get(pk=pk)
        if user.last_login is None:
            user.last_login=datetime.now()
            user.save()
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=pk)
            current_datetime = timezone.now()
            idle_time = current_datetime - user.last_login
            idle_days = idle_time.days
            time_years = idle_days/365.25
            estado_delete = False
            if time_years > 2:
                estado_delete = True
                data = {
                    'state': estado_delete,
                    'url': reverse_lazy('usuarios')
                }
                self.object.delete()
            else:
                data = {
                    'state': estado_delete,
                    'url': reverse_lazy('usuarios')
                }
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuario'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset=None):
        return self.request.user
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar Perfil'
        context['action'] = 'edit'
        context['icon'] = 'fa-user-edit'
        context['url_link'] = self.success_url
        return context
class UserChangePasswordUpdateView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su comtraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva comtraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su comtraseña'
        return form
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar contraseña'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['url_link'] = self.success_url
        return context
class UserChangeGroup(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inicio'))
