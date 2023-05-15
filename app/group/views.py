from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from group.forms import GroupForm
from user.mixins import ValidatePermissionRequiredMinxin


# Create your views here.
class GroupCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/create.html'
    success_url = reverse_lazy('usuarios')
    permission_required = 'add_permission'
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
        context['title'] = 'Nuevo grupo'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['url_link'] = self.success_url
        return context
class NewGroupCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/newcreate.html'
    # success_url = reverse_lazy('usuarios')
    permission_required = 'add_permission'
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
        context['title'] = 'Nuevo grupo'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        return context