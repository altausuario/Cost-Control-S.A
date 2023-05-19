"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from webapp.views import pageNotFound404
from rest_framework.authtoken import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
    path('', include('income.urls')),
    path('', include('expenses.urls')),
    path('', include('categories.urls')),
    path('', include('budget.urls')),
    path('', include('login.urls')),
    path('', include('user.urls')),
    path('', include('group.urls')),
    path('', include('report.urls')),
]

handler404 = pageNotFound404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
