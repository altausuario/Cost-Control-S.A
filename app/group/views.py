from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import *
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.models import Group
from group.forms import GroupForm
from user.mixins import ValidatePermissionRequiredMinxin
# Create your views here.
class GroupListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Group
    template_name = 'group/list.html'
    permission_required = 'view_group'
    url_redirect = reverse_lazy('inicio')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
          action = request.POST['action']
          if action == 'searchdata':
              data = []
              position = 1
              for g in Group.objects.all().order_by('id'):
                  grupo = Group.objects.get(name=g.name)
                  permisos = Permission.objects.filter(group=grupo).order_by('id')
                  pre = []
                  for p in permisos:
                      pre.append(p.name)
                  data.append([
                      position,
                      g.name,
                      pre,
                      g.id
                  ])
                  position += 1
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de permisos'
        context['icon'] = 'fa-list'
        context['create_url'] = reverse_lazy('create_group')
        return context
class GroupCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/create.html'
    success_url = reverse_lazy('list_group')
    permission_required = 'add_group'
    url_redirect = reverse_lazy('inicio')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo grupo de permisos'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['url_link'] = self.success_url
        return context
class GroupUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/create.html'
    success_url = reverse_lazy('list_group')
    permission_required = 'change_group'
    url_redirect = reverse_lazy('inicio')
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
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
        context['title'] = 'Editar gropo de permisos'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['url_link'] = self.success_url
        return context
class GroupDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Group
    template_name = 'group/delete.html'
    success_url = reverse_lazy('list_group')
    permission_required = 'delete_group'
    url_redirect = reverse_lazy('inicio')
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_permissions(self, pk):
        grupo = Group.objects.get(pk=pk)
        permisos = Permission.objects.filter(group=grupo).order_by('id')
        pre = []
        for p in permisos:
            pre.append(p.name)
        return pre
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar grupo de permisos'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        context['permissions'] = self.get_permissions(pk)
        return context

