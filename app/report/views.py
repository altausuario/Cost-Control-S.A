from django.db.models import *
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from budget.models import Budget
from report.forms import ReportBudgetForm
# Create your views here.
class ReportBudgetView(TemplateView):
    template_name = 'report/report_budget.html'
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'search_report_budget':
              start_date = request.POST.get('start_date', '')
              end_date = request.POST.get('end_date', '')
              print(start_date)
              print(end_date)
              search = Budget.objects.all()
              if len(start_date) and len(end_date):
                search = search.filter(date_creation__range=[start_date, end_date], user_id=request.user.id)
              for s in search:
                  data.append([
                      s.id,
                      s.name,
                      s.date_creation.strftime('%Y-%m-%d'),
                      format(s.total_income, '.2f'),
                      format(s.total_expenses, '.2f'),
                      format(s.total, '.2f'),
                  ])
              income_total = search.aggregate(r=Coalesce(Sum('total_income'), 0, output_field=DecimalField())).get('r')
              expenses_total = search.aggregate(r=Coalesce(Sum('total_expenses'), 0, output_field=DecimalField())).get('r')
              total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
              data.append([
                  '---',
                  '---',
                  '----',
                  format(income_total, '.2f'),
                  format(expenses_total, '.2f'),
                  format(total, '.2f'),
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