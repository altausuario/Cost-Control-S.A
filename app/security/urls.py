from django.urls import path
from security.views import *

urlpatterns = [
    path('access/users/list/', AccessUsersListView.as_view(), name='list_security'),
    path('access/users/delete/<int:pk>', AccessUsersDeleteView.as_view(), name='delete_security'),
]