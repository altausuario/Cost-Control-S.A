from django.urls import path

from group.views import *
from webapp.views import *

urlpatterns = [
    path('text/', GroupCreateView.as_view(), name='prueba'),
    path('group/add', NewGroupCreateView.as_view(), name='newGroup')
]