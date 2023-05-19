from django.urls import path
from login.views import *

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('reset/password/', ResetPasswordView.as_view(), name='resetPassword'),
    path('create/new/user/', NewUserProfileView.as_view(), name='new_user_profile'),
    path('reset/change/password/<str:token>/', ChangePasswordView.as_view(), name='resetChangePassword'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
]