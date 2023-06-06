from django.urls import path
from user.views import *
urlpatterns = [
    path('list/usuarios/', UserListView.as_view(), name='usuarios'),
    path('list/usuarios/add/', UserCreateView.as_view(), name='addUsuarios'),
    path('list/usuarios/edit/<int:pk>', UserUpdateView.as_view(), name='editUsuarios'),
    path('list/usuarios/delete/<int:pk>', UserDeleteView.as_view(), name='deleteUsuarios'),
    path('change/profile/', UserProfileUpdateView.as_view(), name='profileUsuarios'),
    path('change/password/', UserChangePasswordUpdateView.as_view(), name='changePasswordUser'),
    path('change/group/<int:pk>', UserChangeGroup.as_view(), name='changeGroup'),
]