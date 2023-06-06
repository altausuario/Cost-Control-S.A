from django.urls import path
from budget.views import *
urlpatterns = [
    path('budget/list/', BudgetListView.as_view(), name='list_budget'),
    path('budget/create/', BudgetCreateView.as_view(), name='create_budget'),
    path('budget/update/<int:pk>', BudgetUpdateView.as_view(), name='delete_budget'),
    path('budget/delete/<int:pk>', BudgetDeleteView.as_view(), name='delete_budget'),
    path('budget/invoice/pdf/<int:pk>', BudgetInvoicePdfView.as_view(), name='invoice_pdf_budget')
]