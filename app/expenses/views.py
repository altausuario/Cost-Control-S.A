from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from categories.models import Categories
from expenses.forms import ExpensesForm
from expenses.models import Expenses
from user.mixins import ValidatePermissionRequiredMinxin


# Create your views here.

class ExpensesListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Expenses
    template_name = 'expenses/list.html'
    permission_required = 'view_expenses'

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
              for i in Expenses.objects.filter(user_id=request.user.id).order_by('id'):
                  item = i.toJSON()
                  item['position'] = position
                  for c in Categories.objects.filter(id=i.user_id):
                      name = c.name
                      item['categorie'] = name
                      data.append(item)
                  position += 1
              print(data)
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de gastos'
        context['icon'] = 'fa-search'
        context['url_link'] = reverse_lazy('budget')
        context['create_url'] = reverse_lazy('create_expenses')
        return context
class ExpensesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Expenses
    form_class = ExpensesForm
    template_name = 'expenses/create.html'
    success_url = reverse_lazy('list_expenses')
    permission_required = 'add_expenses'
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
        context['title'] = 'Nuevo gasto'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['url_link'] = self.success_url
        return context
class ExpensesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Expenses
    form_class = ExpensesForm
    template_name = 'expenses/create.html'
    success_url = reverse_lazy('list_expenses')
    permission_required = 'change_expenses'
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
        context['title'] = 'Editar gasto'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['url_link'] = self.success_url
        return context
class ExpensesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Expenses
    template_name = 'expenses/delete.html'
    success_url = reverse_lazy('list_expenses')
    permission_required = 'delete_expenses'
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
        context['title'] = 'Eliminar gasto'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context