import json
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
from categories.models import Categories
from expenses.models import Expenses
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
        context['icon'] = 'fa-list'
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
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo presupuesto'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['detIncome'] = []
        context['detExpenses'] = []
        context['url_link'] = self.success_url
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
                        'state': i.state,
                        'annotations': i.annotations,
                        'date_creation': i.date_creation.strftime('%Y-%m-%d'),
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
                        'state': e.state,
                        'annotations': e.annotations,
                        'date_creation': e.date_creation.strftime('%Y-%m-%d'),
                    })
        except:
            pass
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar presupuesto'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['detIncome'] = json.dumps(self.get_details_income())
        context['detExpenses'] = json.dumps(self.get_details_Expenses())
        context['url_link'] = self.success_url
        return context
class BudgetDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Budget
    template_name = 'budget/delete.html'
    success_url = reverse_lazy('list_budget')
    permission_required = 'delete_budget'
    url_redirect = reverse_lazy('inicio')

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
        context['icon'] = 'fa-trash-alt'
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
    def get_invoice_total_expenses(self, pk):
        data = 0
        for b in Budget.objects.filter(id=pk):
            for ec in ExpensesConetion.objects.filter(budget_id=b.id):
                for e in Expenses.objects.filter(id=ec.expenses_id).order_by('id'):
                    data += e.amount
        return data
    def get_invoice_total_income(self, pk):
        data = 0
        for b in Budget.objects.filter(id=pk):
            for ic in IncomeConetion.objects.filter(budget_id=b.id):
                for i in Income.objects.filter(id=ic.income_id).order_by('id'):
                    data += i.amount
        return data
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
                    'total_income': self.get_invoice_total_income(id),
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