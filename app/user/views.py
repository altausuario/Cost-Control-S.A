from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create user'
        context['action'] = 'add'
        context['icon'] = 'fa-user-plus'
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

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.id == 1:
            return HttpResponseRedirect(reverse_lazy('usuarios'))
        return super().dispatch(request, *args, **kwargs)

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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['action'] = 'edit'
        context['icon'] = 'fa-user-edit'
        context['url_link'] = self.success_url
        context['formGruop'] = GroupForm
        return context
class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('usuarios')
    permission_required = 'delete_user'
    url_redirect = reverse_lazy('usuarios')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.id == 1:
            return HttpResponseRedirect(reverse_lazy('usuarios'))
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
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
        context['title'] = 'Actualizar usuario'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['url_link'] = self.success_url
        return context
class UserChangePasswordUpdateView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

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