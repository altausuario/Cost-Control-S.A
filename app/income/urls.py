from django.urls import path

from income.views import *

urlpatterns = [
    path('incomes/list/', IncomeListView.as_view(), name='list_income'),
    path('incomes/create/', IncomeCreateView.as_view(), name='create_income'),
    path('incomes/update/<int:pk>', IncomeUpdateView.as_view(), name='update_income'),
    path('incomes/delete/<int:pk>', IncomeDeleteView.as_view(), name='delete_income')
]