from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from budget.models import *
from categories.models import Categories
from expenses.forms import ExpensesForm
from expenses.models import Expenses
from user.mixins import ValidatePermissionRequiredMinxin
# Create your views here.
class ExpensesListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Expenses
    template_name = 'expenses/list.html'
    permission_required = 'view_expenses'

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
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de gastos'
        context['icon'] = 'fa-list'
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
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                pku = 0
                pki = Expenses.objects.filter(id=self.kwargs.get('pk'))
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
            pki = Expenses.objects.filter(id=self.kwargs.get('pk'))
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
        context['title'] = 'Eliminar gasto'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context