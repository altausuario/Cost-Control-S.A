from django.urls import path
from categories.views import *
urlpatterns = [
    path('categories/list/', CategoriesListView.as_view(), name='list_categories'),
    path('categories/create/', CategoriesCreateView.as_view(), name='create_categories'),
    path('categories/update/<int:pk>', CategoriesUpdateView.as_view(), name='update_categories'),
    path('categories/delete/<int:pk>', CategoriesDeleteView.as_view(), name='delete_categories')
]