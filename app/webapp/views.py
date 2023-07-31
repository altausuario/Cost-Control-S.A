from _pydecimal import Decimal
from datetime import datetime
from crum import get_current_request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from budget.models import Budget
from random import randint
from webapp.forms import *
# Create your views here.
class homeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def meses_año(self):
        data = '';
        month = datetime.now().month.real
        if month == 1:
            data = 'Enero'
        elif month == 2:
            data = 'Febrero'
        elif month == 3:
            data = 'Marzo'
        elif month == 4:
            data = 'Abril'
        elif month == 5:
            data = 'Mayo'
        elif month == 6:
            data = 'Junio'
        elif month == 7:
            data = 'Julio'
        elif month == 8:
            data = 'Agosto'
        elif month == 9:
            data = 'Septiembre'
        elif month == 10:
            data = 'Octubre'
        elif month == 11:
            data = 'Noviembre'
        elif month == 12:
            data = 'Diciembre'
        return data
    def get_graph_budget_year_month(self):
        data = []
        request = get_current_request()
        try:
            year = datetime.now().year
            for m in range(1, 13):
                presupuestoTotal = Budget.objects.filter(date_creation__year=year, date_creation__month=m, user_id=request.user.id).aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                data.append(float(presupuestoTotal))
        except Exception as e:
            print(f'error: {e}')
        return data
    def get_graph_income_year_month(self):
        data = []
        request = get_current_request()
        try:
            year = datetime.now().year
            for m in range(1, 13):
                presupuestoTotal = Budget.objects.filter(date_creation__year=year, date_creation__month=m, user_id=request.user.id).aggregate(r=Coalesce(Sum('total_income'), 0, output_field=DecimalField())).get('r')
                data.append(float(presupuestoTotal))
        except Exception as e:
            print(f'error: {e}')
        return data
    def get_graph_expenses_year_month(self):
        data = []
        request = get_current_request()
        try:
            year = datetime.now().year
            for m in range(1, 13):
                presupuestoTotal = Budget.objects.filter(date_creation__year=year, date_creation__month=m, user_id=request.user.id).aggregate(r=Coalesce(Sum('total_expenses'), 0, output_field=DecimalField())).get('r')
                data.append(float(presupuestoTotal))
        except Exception as e:
            print(f'error: {e}')
        return data
    def get_graph_budget_percentage_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        request = get_current_request()
        try:
            for b in Budget.objects.all():
                Total = Budget.objects.filter(date_creation__year=year, date_creation__month=month, user_id=request.user.id, id=b.id).aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                if Total > 0:
                    data.append({
                        'name': b.name,
                        'y': float(Total)
                    })
                    Total = 0
        except:
            pass
        return data
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'get_graph_budget_year_month':
              data = {'name': 'Presupuesto', 'color': '#0000FF', 'data': self.get_graph_budget_year_month()}
          elif action == 'get_graph_income_year_month':
              data = {'name': 'Ingresos', 'color': '#00FF00', 'data': self.get_graph_income_year_month()}
          elif action == 'get_graph_expenses_year_month':
              data = {'name': 'Egresos', 'color': '#FF0000', 'data': self.get_graph_expenses_year_month()}

          elif action == 'get_graph_budget_percentage_year_month':
              data = {
                  'name': 'Porcentaje',
                  'colorByPoint': True,
                  'data': self.get_graph_budget_percentage_year_month()
              }
              print(data)
          elif action == 'get_graph_online':
              data = {'y': randint(1, 100)}
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get(self, request, *args, **kwargs):
        request.user.get_goup_session()
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['icon'] = 'fa-home'
        context['año'] = datetime.now().year.real
        context['mes'] = self.meses_año()
        return context
def pageNotFound404(request, exception):
    return render(request, '404.html')
