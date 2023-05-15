from django.urls import path

from expenses.views import *

urlpatterns = [
    path('expenses/list/', ExpensesListView.as_view(), name='list_expenses'),
    path('expenses/create/', ExpensesCreateView.as_view(), name='create_expenses'),
    path('expenses/update/<int:pk>', ExpensesUpdateView.as_view(), name='update_expenses'),
    path('expenses/delete/<int:pk>', ExpensesDeleteView.as_view(), name='delete_expenses')
]