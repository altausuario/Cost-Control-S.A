import json
from django import template
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from budget.forms import PresupuestoForm
from budget.models import *
from categories.forms import CategoriesForm
from categories.models import Categories
from expenses.models import Expenses
from income.forms import IncomeForm
from income.models import Income
from user.mixins import ValidatePermissionRequiredMinxin
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
# Create your views here.
class BudgetListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Budget
    template_name = 'budget/list.html'
    permission_required = 'view_budget'
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
              for i in Budget.objects.filter(user_id=request.user.id).order_by('id'):
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
        context['title'] = 'Lista de presupuesto'
        context['icon'] = 'fa-bars-staggered mr-1'
        context['url_link'] = reverse_lazy('budget')
        context['create_url'] = reverse_lazy('create_budget')
        return context
class BudgetCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Budget
    form_class = PresupuestoForm
    template_name = 'budget/create.html'
    success_url = reverse_lazy('list_budget')
    permission_required = 'add_budget'
    url_redirect = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_conversor(self, amount):
        valor_convertido = float(amount.replace("$", "").replace("\xa0", "").replace(".", "").replace(",", "."))
        return valor_convertido
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                     evens = json.loads(request.POST['vents'])
                     budget = Budget()
                     budget.name = evens['name']
                     budget.total_income = float(evens['total_income'])
                     budget.total_expenses = float(evens['total_expenses'])
                     budget.total = float(evens['total'])
                     budget.save()

                     for i in evens['incomes']:
                         ic = IncomeConetion()
                         ic.budget_id = budget.id
                         ic.income_id = i['id']
                         ic.save()

                     for e in evens['expenses']:
                         ec = ExpensesConetion()
                         ec.budget_id = budget.id
                         ec.expenses_id = e['id']
                         ec.save()
            elif action == 'autocomplete':
                data = []

                for i in Income.objects.filter(description__icontains=request.POST['term'], user_id=request.user.id)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.description
                    data.append(item)
            elif action == 'autocompleteExpenses':
                data = []
                for i in Expenses.objects.filter(description__icontains=request.POST['term'], user_id=request.user.id)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.description
                    data.append(item)
            elif action == 'Ingreso':
                with transaction.atomic():
                    income = Income()
                    income.description = request.POST['description']
                    income.annotations = request.POST['annotations']
                    income.date_joined = request.POST['date_joined']
                    income.categorie_id = request.POST['categorie']
                    income.state = request.POST['state']
                    income.amount = self.get_conversor(request.POST['amount'])
                    income.iva = request.POST['iva']
                    income.totaliva = self.get_conversor(request.POST['totaliva'])
                    income.total = self.get_conversor(request.POST['totalRegister'])
                    income.image = request.POST['image']
                    income.user_id = request.user.id
                    income.save()
                    json_income = json.dumps({
                        'id': income.id,
                        'description': income.description,
                        'annotations': income.annotations,
                        'date_joined': income.date_joined,
                        'categorie_id': income.categorie_id,
                        'state': income.state,
                        'amount': income.amount,
                        'iva': income.iva,
                        'totaliva': income.totaliva,
                        'total': income.total,
                        'user_id': income.user_id,
                    })
                    data = json.loads(json_income)
            elif action == 'Gasto':
                expense = Expenses()
                expense.description = request.POST['description']
                expense.annotations = request.POST['annotations']
                expense.date_joined = request.POST['date_joined']
                expense.categorie_id = request.POST['categorie']
                expense.state = request.POST['state']
                expense.amount = self.get_conversor(request.POST['amount'])
                expense.iva = request.POST['iva']
                expense.totaliva = self.get_conversor(request.POST['totaliva'])
                expense.total = self.get_conversor(request.POST['totalRegister'])
                expense.image = request.POST['image']
                expense.user_id = request.user.id
                expense.save()
                json_expenses = json.dumps({
                    'id': expense.id,
                    'description': expense.description,
                    'annotations': expense.annotations,
                    'date_joined': expense.date_joined,
                    'categorie_id': expense.categorie_id,
                    'state': expense.state,
                    'amount': expense.amount,
                    'iva': expense.iva,
                    'totaliva': expense.totaliva,
                    'total': expense.total,
                    'user_id': expense.user_id,
                })
                data = json.loads(json_expenses)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo presupuesto'
        context['action'] = 'add'
        context['icon'] = 'fa-plus mr-1'
        context['img'] = 'facture.png'
        context['detIncome'] = []
        context['detExpenses'] = []
        context['url_link'] = self.success_url
        context['register'] = IncomeForm
        return context
class BudgetUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Budget
    form_class = PresupuestoForm
    template_name = 'budget/create.html'
    success_url = reverse_lazy('list_budget')
    permission_required = 'change_budget'
    url_redirect = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def get_conversor(self, amount):
        valor_convertido = float(amount.replace("$", "").replace("\xa0", "").replace(".", "").replace(",", "."))
        return valor_convertido
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                with transaction.atomic():
                    evens = json.loads(request.POST['vents'])
                    pku = 0
                    pki = Budget.objects.filter(id=self.kwargs.get('pk'))
                    for i in pki:
                        pku = i.user_id
                    if pku == request.user.id:
                        budget = self.get_object()
                        budget.name = evens['name']
                        budget.total_income = float(evens['total_income'])
                        budget.total_expenses = float(evens['total_expenses'])
                        budget.total = float(evens['total'])
                        budget.save()
                        for i in IncomeConetion.objects.filter(budget_id=budget.id):
                            i.delete()

                        for i in evens['incomes']:
                            ic = IncomeConetion()
                            ic.budget_id = budget.id
                            ic.income_id = i['id']
                            ic.save()

                        for e in ExpensesConetion.objects.filter(budget_id=budget.id):
                            e.delete()

                        for e in evens['expenses']:
                            ec = ExpensesConetion()
                            ec.budget_id = budget.id
                            ec.expenses_id = e['id']
                            ec.save()
                    else:
                        data['error'] = 'No tienes las credenciales correspondientes'
            elif action == 'Ingreso':
                with transaction.atomic():
                    income = Income()
                    income.description = request.POST['description']
                    income.annotations = request.POST['annotations']
                    income.date_joined = request.POST['date_joined']
                    income.categorie_id = request.POST['categorie']
                    income.state = request.POST['state']
                    income.amount = self.get_conversor(request.POST['amount'])
                    income.iva = request.POST['iva']
                    income.totaliva = self.get_conversor(request.POST['totaliva'])
                    income.total = self.get_conversor(request.POST['totalRegister'])
                    income.image = request.POST['image']
                    income.user_id = request.user.id
                    income.save()
                    json_income = json.dumps({
                        'id': income.id,
                        'description': income.description,
                        'annotations': income.annotations,
                        'date_joined': income.date_joined,
                        'categorie_id': income.categorie_id,
                        'state': income.state,
                        'amount': income.amount,
                        'iva': income.iva,
                        'totaliva': income.totaliva,
                        'total': income.total,
                        'user_id': income.user_id,
                    })
                    data = json.loads(json_income)
            elif action == 'Gasto':
                with transaction.atomic():
                    expense = Expenses()
                    expense.description = request.POST['description']
                    expense.annotations = request.POST['annotations']
                    expense.date_joined = request.POST['date_joined']
                    expense.categorie_id = request.POST['categorie']
                    expense.state = request.POST['state']
                    expense.amount = self.get_conversor(request.POST['amount'])
                    expense.iva = request.POST['iva']
                    expense.totaliva = self.get_conversor(request.POST['totaliva'])
                    expense.total = self.get_conversor(request.POST['totalRegister'])
                    expense.image = request.POST['image']
                    expense.user_id = request.user.id
                    expense.save()
                    json_expenses = json.dumps({
                        'id': expense.id,
                        'description': expense.description,
                        'annotations': expense.annotations,
                        'date_joined': expense.date_joined,
                        'categorie_id': expense.categorie_id,
                        'state': expense.state,
                        'amount': expense.amount,
                        'iva': expense.iva,
                        'totaliva': expense.totaliva,
                        'total': expense.total,
                        'user_id': expense.user_id,
                    })
                    data = json.loads(json_expenses)
            elif action == 'autocomplete':
                data = []
                for i in Income.objects.filter(description__icontains=request.POST['term'], user_id=request.user.id)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.description
                    data.append(item)
            elif action == 'autocompleteExpenses':
                data = []
                for i in Expenses.objects.filter(description__icontains=request.POST['term'], user_id=request.user.id)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.description
                    data.append(item)
            elif action == 'search_categories':
                data = []
                categories = Categories.objects.filter(name__icontains=request.POST['term'])[0:10]
                for cat in categories:
                    item = cat.toJSON()
                    item['text'] = cat.name
                    data.append(item)
            elif action == 'create_categories':
                with transaction.atomic():
                    frmCategories = CategoriesForm(request.POST)
                    data = frmCategories.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_details_income(self):
        data = []
        try:
            for ic in IncomeConetion.objects.filter(budget_id=self.get_object().id):
                inc = ic.income_id
                for i in Income.objects.filter(id=inc):
                    data.append({
                        'id': i.id,
                        'description': i.description,
                        'amount': float(i.amount),
                        'iva': float(i.iva),
                        'totaliva': float(i.totaliva),
                        'total': float(i.total),
                        'state': i.state,
                        'annotations': i.annotations,
                        'date_joined': i.date_joined.strftime('%Y-%m-%d'),
                    })
        except:
            pass
        return data
    def get_details_Expenses(self):
        data = []
        try:
            for ec in ExpensesConetion.objects.filter(budget_id=self.get_object().id):
                exp = ec.expenses_id
                for e in Expenses.objects.filter(id=exp):
                    data.append({
                        'id': e.id,
                        'description': e.description,
                        'amount': float(e.amount),
                        'iva': float(e.iva),
                        'totaliva': float(e.totaliva),
                        'total': float(e.total),
                        'state': e.state,
                        'annotations': e.annotations,
                        'date_joined': e.date_joined.strftime('%Y-%m-%d'),
                    })
        except:
            pass
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar presupuesto'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit mr-1'
        context['img'] = 'facture.png'
        context['detIncome'] = json.dumps(self.get_details_income())
        context['detExpenses'] = json.dumps(self.get_details_Expenses())
        context['url_link'] = self.success_url
        context['register'] = IncomeForm
        context['cat'] = CategoriesForm
        return context
class BudgetDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Budget
    template_name = 'budget/delete.html'
    success_url = reverse_lazy('list_budget')
    permission_required = 'delete_budget'
    url_redirect = reverse_lazy('inicio')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pku = 0
            pki = Budget.objects.filter(id=self.kwargs.get('pk'))
            for i in pki:
                pku = i.user_id
            if pku == request.user.id:
                self.object.delete()
            else:
                data['error'] = 'No tienes los permisos correspondientes'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar presupuesto'
        context['icon'] = 'fa-trash-alt mr-1'
        context['url_link'] = self.success_url
        return context
class BudgetInvoicePdfView(LoginRequiredMixin, View):
    def get_invoice_income(self, pk):
        data = []
        for b in Budget.objects.filter(id=pk):
            for ic in IncomeConetion.objects.filter(budget_id=b.id):
                for i in Income.objects.filter(id=ic.income_id).order_by('id'):
                    item = i.toJSON()
                    item['categorie'] = i.categorie
                    data.append(item)
        return data
    def get_invoice_expenses(self, pk):
        data = []
        for b in Budget.objects.filter(id=pk):
            for ec in ExpensesConetion.objects.filter(budget_id=b.id):
                for e in Expenses.objects.filter(id=ec.expenses_id).order_by('id'):
                    item = e.toJSON()
                    item['categorie'] = e.categorie
                    data.append(item)
        return data
    def get_invoice_total_amount_expenses(self, pk):
        amount = 0
        total_iva = 0
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ec in ExpensesConetion.objects.filter(budget_id=b.id):
                for e in Expenses.objects.filter(id=ec.expenses_id).order_by('id'):
                    amount += e.amount
                    total_iva += e.totaliva
                    total += total
        return amount
    def get_invoice_total_iva_expenses(self, pk):
        amount = 0
        total_iva = 0
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ec in ExpensesConetion.objects.filter(budget_id=b.id):
                for e in Expenses.objects.filter(id=ec.expenses_id).order_by('id'):
                    amount += e.amount
                    total_iva += e.totaliva
                    total += total
        return total_iva
    def get_invoice_total_expenses(self, pk):
        amount = 0
        total_iva = 0
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ec in ExpensesConetion.objects.filter(budget_id=b.id):
                for e in Expenses.objects.filter(id=ec.expenses_id).order_by('id'):
                    amount += e.amount
                    total_iva += e.totaliva
                    total += e.total
        return total
    def get_invoice_total_amount_income(self, pk):
        data = []
        amount = 0
        total_iva=0
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ic in IncomeConetion.objects.filter(budget_id=b.id):
                for i in Income.objects.filter(id=ic.income_id).order_by('id'):
                    amount += i.amount
                    total_iva += i.totaliva
                    total += i.total
        return amount
    def get_invoice_total_iva_income(self, pk):
        data = []
        amount = 0
        total_iva=0
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ic in IncomeConetion.objects.filter(budget_id=b.id):
                for i in Income.objects.filter(id=ic.income_id).order_by('id'):
                    amount += i.amount
                    total_iva += i.totaliva
                    total += i.total
        return total_iva
    def get_invoice_total_income(self, pk):
        data = []
        total = 0
        for b in Budget.objects.filter(id=pk):
            for ic in IncomeConetion.objects.filter(budget_id=b.id):
                for i in Income.objects.filter(id=ic.income_id).order_by('id'):
                    total += i.total
        print(total)
        return total
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATIC_ROOT
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path
    def get(self, request, *args, **kwargs):
        try:
            budget = Budget.objects.get(pk=self.kwargs['pk'])
            if budget.user_id == request.user.id:
                template = get_template('budget/invoice.html')
                id = self.kwargs['pk']
                context = {
                    'budget': Budget.objects.get(pk=self.kwargs['pk']),
                    'date_joined':datetime.now(),
                    'cli_names': request.user.first_name + ' ' + request.user.last_name,
                    'income': self.get_invoice_income(id),
                    'expenses': self.get_invoice_expenses(id),
                    'total_amount_income': self.get_invoice_total_amount_income(id),
                    'total_iva_income': self.get_invoice_total_iva_income(id),
                    'total_income': self.get_invoice_total_income(id),
                    'total_amount_expenses': self.get_invoice_total_amount_expenses(id),
                    'total_iva_expenses': self.get_invoice_total_iva_expenses(id),
                    'total_expenses': self.get_invoice_total_expenses(id),
                    'comp': {
                        'name': 'Cost Control S.A.',
                        'address': 'Bucaramanga, Santander'

                    },
                    'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png'),
                    'title': 'PDF'
                }
                html = template.render(context)
                response = HttpResponse(content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
                pisa_status = pisa.CreatePDF(
                    html, dest=response,
                    link_callback=self.link_callback
                )
                return response
            else:
                return HttpResponseRedirect(reverse_lazy('list_budget'))
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('list_budget'))