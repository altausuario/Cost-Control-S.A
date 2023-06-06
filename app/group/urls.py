from django.urls import path
from group.views import *
from webapp.views import *
urlpatterns = [
    path('list/group', GroupListView.as_view(), name='list_group'),
    path('create/group', GroupCreateView.as_view(), name='create_group'),
    path('update/group/<int:pk>', GroupUpdateView.as_view(), name='update_group'),
    path('delete/group/<int:pk>', GroupDeleteView.as_view(), name='delete_group'),
]