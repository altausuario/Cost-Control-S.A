from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from budget.models import *
from categories.models import Categories
from income.forms import IncomeForm
from income.models import Income
from user.mixins import ValidatePermissionRequiredMinxin
# Create your views here.
class IncomeListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Income
    template_name = 'income/list.html'
    permission_required = 'view_income'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
          action = request.POST['action']
          if action == 'searchdata':
              data = []
              position = 1
              for i in Income.objects.filter(user_id=request.user.id).order_by('id'):
                  item = i.toJSON()
                  item['position'] = position
                  for c in Categories.objects.filter(id=i.user_id):
                      name = c.name
                      item['categorie'] = name
                      data.append(item)
                  position += 1
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ingresos'
        context['icon'] = 'fa-list'
        context['url_link'] = reverse_lazy('budget')
        context['create_url'] = reverse_lazy('create_income')
        return context
class IncomeCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/create.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'add_income'
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
        context['title'] = 'Nuevo ingreso'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['img'] = 'facture.png'
        context['url_link'] = self.success_url
        return context
class IncomeUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/create.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'change_income'
    url_redirect = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def get_calcular(self):
        budget = Budget.objects.all().order_by('id')
        total_ex = 0
        total_in = 0
        total = 0
        for b in budget:
            exc = ExpensesConetion.objects.filter(budget_id=b.id)
            for ec in exc:
                ex = Expenses.objects.filter(id=ec.expenses_id)
                for e in ex:
                    total_ex += e.total
            inc = IncomeConetion.objects.filter(budget_id=b.id)
            for inm in inc:
                ino = Income.objects.filter(id=inm.income_id)
                for i in ino:
                    total_in += i.total

            total = total_in - total_ex
            but =Budget()
            but.id = b.id
            but.name = b.name
            but.date_creation = b.date_creation
            but.total_income = total_in
            but.total_expenses = total_ex
            but.total = total
            but.save()
            total_ex = 0
            total_in = 0
        return ''

    def image_income(self, pk):
        income = Income.objects.get(pk=pk)
        if not income.image:
            return 'facture.png'
        return income.image
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                pku = 0
                pki = Income.objects.filter(id=self.kwargs.get('pk'))
                for i in pki:
                    pku = i.user_id
                if pku == request.user.id:
                    form = self.get_form()
                    data = form.save()
                    self.get_calcular()
                else:
                    data['error'] = 'No tienes las credenciales correspondientes'
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['title'] = 'Editar ingreso'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['img'] = self.image_income(pk)
        context['url_link'] = self.success_url
        return context
class IncomeDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Income
    template_name = 'income/delete.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'delete_income'
    url_redirect = reverse_lazy('inicio')
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def get_calcular(self):
        budget = Budget.objects.all().order_by('id')
        total_ex = 0
        total_in = 0
        total = 0
        for b in budget:
            exc = ExpensesConetion.objects.filter(budget_id=b.id)
            for ec in exc:
                ex = Expenses.objects.filter(id=ec.expenses_id)
                for e in ex:
                    total_ex += e.amount
            print(f'Expenses {total_ex}')

            inc = IncomeConetion.objects.filter(budget_id=b.id)
            for inm in inc:
                ino = Income.objects.filter(id=inm.income_id)
                for i in ino:
                    total_in += i.amount
            print(f'Incomes {total_in}')

            total = total_in - total_ex
            but =Budget()
            but.id = b.id
            but.name = b.name
            but.date_creation = b.date_creation
            but.total_income = total_in
            but.total_expenses = total_ex
            but.total = total
            but.save()
            total_ex = 0
            total_in = 0
        return ''
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pku = 0
            pki = Income.objects.filter(id=self.kwargs.get('pk'))
            for i in pki:
                pku = i.user_id
            if pku == request.user.id:
                self.object.delete()
                self.get_calcular()
            else:
                data['error'] = 'No tienes los permisos correspondientes'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar ingreso'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context