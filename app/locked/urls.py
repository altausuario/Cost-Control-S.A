from django.urls import path

from income.views import *
from locked.views import *

urlpatterns = [
    path('user/inative/list/', LockedListView.as_view(), name='list_locked'),
    path('user/activate/', LockedActivateFormView.as_view(), name='activate_locked'),
    path('activate/account/user/<str:token>/', ChangeActivateUserView.as_view(), name='activateAccountUser'),
]