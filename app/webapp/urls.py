from django.urls import path

from group.views import GroupCreateView
from webapp.views import *

urlpatterns = [
    path('Dashboard/', homeView.as_view(), name='inicio'),
    # path('text/', GroupCreateView().as_view(), name='prueba')
]