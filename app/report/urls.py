from django.urls import path
from report.views import ReportBudgetView

urlpatterns = [
    path('report/budget/', ReportBudgetView.as_view(), name='report_budget'),
]