import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import *
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from budget.models import Budget
from categories.models import Categories
from expenses.models import Expenses
from income.models import Income
from report.forms import ReportBudgetForm
from user.mixins import ValidatePermissionRequiredMinxin
# Create your views here.
class ReportBudgetView(LoginRequiredMixin,TemplateView):
    template_name = 'report/report_budget.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def currency_format(self, value):
        try:
            value = float(value)
            return "$ {:,.2f}".format(value).replace(",", ".")
        except (ValueError, TypeError):
            return value
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'search_report_budget':
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              search = Budget.objects.all()
              position = 1
              if len(start_date) and len(end_date):
                search = search.filter(date_creation__range=[start_date, end_date], user_id=request.user.id)
              for s in search:
                  data.append([
                      position,
                      s.name,
                      s.date_creation.strftime('%Y-%m-%d'),
                      self.currency_format(s.total_income),
                      self.currency_format(s.total_expenses),
                      self.currency_format(s.total),
                  ])
                  position += 1
              income_total = search.aggregate(r=Coalesce(Sum('total_income'), 0, output_field=DecimalField())).get('r')
              expenses_total = search.aggregate(r=Coalesce(Sum('total_expenses'), 0, output_field=DecimalField())).get('r')
              total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
              data.append([
                  '',
                  '---',
                  '----',
                  self.currency_format(income_total),
                  self.currency_format(expenses_total),
                  self.currency_format(total),
              ])
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de presupuesto'
        context['icon'] = 'fa-chart-bar'
        context['link_url'] = reverse_lazy('report_budget')
        context['form'] = ReportBudgetForm
        return context
class ReportIncomesView(LoginRequiredMixin, TemplateView):
    template_name = 'report/report_income.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def currency_format(self, value):
        try:
            value = float(value)
            return "$ {:,.2f}".format(value).replace(",", ".")
        except (ValueError, TypeError):
            return value
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'search_report_budget':
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              search = Income.objects.all()
              position = 1
              if len(start_date) and len(end_date):
                search = search.filter(date_joined__range=[start_date, end_date], user_id=request.user.id)
              for s in search:
                  c = s.categorie.id
                  n = Categories.objects.get(id=c)
                  data.append([
                      position,
                      s.description,
                      s.date_joined.strftime('%Y-%m-%d'),
                      n.name,
                      s.state,
                      self.currency_format(s.amount),
                      format(s.iva, '.0f'),
                      self.currency_format(s.totaliva),
                      self.currency_format(s.total),
                  ])
                  position += 1
              income_total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
              data.append([
                  '---',
                  '---',
                  '----',
                  '----',
                  '----',
                  '----',
                  '----',
                  f'----',
                  self.currency_format(income_total),
              ])
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,  safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de ingresos'
        context['icon'] = 'fa-chart-bar'
        context['link_url'] = reverse_lazy('report_incomes')
        context['form'] = ReportBudgetForm
        return context
class ReportExpensesView(LoginRequiredMixin,TemplateView):
    template_name = 'report/report_expenses.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def currency_format(self, value):
        try:
            value = float(value)
            return "$ {:,.2f}".format(value).replace(",", ".")
        except (ValueError, TypeError):
            return value
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'search_report_budget':
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              search = Expenses.objects.all()
              name = '';
              position = 1
              if len(start_date) and len(end_date):
                search = search.filter(date_joined__range=[start_date, end_date], user_id=request.user.id)
              for s in search:
                  c = s.categorie.id
                  n = Categories.objects.get(id=c)
                  data.append([
                      position,
                      s.description,
                      s.date_joined.strftime('%Y-%m-%d'),
                      n.name,
                      s.state,
                      self.currency_format(s.amount),
                      format(s.iva, '.0f'),
                      self.currency_format(s.totaliva),
                      self.currency_format(s.total),
                  ])
                  position += 1
              income_total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
              data.append([
                  '---',
                  '---',
                  '----',
                  '----',
                  '----',
                  '----',
                  '----',
                  '----',
                  self.currency_format(income_total),
              ])
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,  safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de gastos'
        context['icon'] = 'fa-chart-bar'
        context['link_url'] = reverse_lazy('report_expenses')
        context['form'] = ReportBudgetForm
        return context