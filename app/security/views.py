from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from report.forms import ReportBudgetForm
from security.choices import LOGIN_TYPE
from security.models import AccessUsers
from user.mixins import ValidatePermissionRequiredMinxin
from user.models import User


# Create your views here.
class AccessUsersListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, FormView):
    form_class = ReportBudgetForm
    template_name = 'security/list.html'
    permission_required = 'view_accessusers'
    url_redirect = reverse_lazy('inicio')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = AccessUsers.objects.all().order_by('id')
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Accesos de Usuarios'
        context['icon'] = 'fa-chart-bar'
        context['list_url'] = reverse_lazy('access_users_list')
        context['entity'] = 'Accesos de Usuarios'
        return context

class AccessUsersDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = AccessUsers
    template_name = 'security/delete.html'
    success_url = reverse_lazy('list_security')
    permission_required = 'delete_accessusers'
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Accesos de Usuarios'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context