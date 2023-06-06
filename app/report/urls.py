from django.urls import path
from report.views import *
urlpatterns = [
    path('report/budget/', ReportBudgetView.as_view(), name='report_budget'),
    path('report/incomes/', ReportIncomesView.as_view(), name='report_incomes'),
    path('report/expenses/', ReportExpensesView.as_view(), name='report_expenses'),
]