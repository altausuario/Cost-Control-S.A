from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from categories.forms import CategoriesForm
from categories.models import Categories
from user.mixins import ValidatePermissionRequiredMinxin

# Create your views here.

class CategoriesListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Categories
    template_name = 'categories/list.html'
    permission_required = 'view_categories'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
          action = request.POST['action']
          if action == 'searchdata':
              data = []
              position = 1
              for i in Categories.objects.filter(user_id=request.user.id).order_by('id'):
                  item = i.toJSON()
                  item['position'] = position
                  data.append(item)
                  position += 1
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de categorias'
        context['icon'] = 'fa-list'
        context['url_link'] = reverse_lazy('budget')
        context['create_url'] = reverse_lazy('create_categories')
        return context

class CategoriesCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'categories/create.html'
    success_url = reverse_lazy('list_categories')
    permission_required = 'add_categories'
    url_redirect = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva categoria'
        context['action'] = 'add'
        context['icon'] = 'fa-plus'
        context['url_link'] = self.success_url
        return context
class CategoriesUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'categories/create.html'
    success_url = reverse_lazy('list_categories')
    permission_required = 'change_categories'
    url_redirect = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                pku = 0
                pki = Categories.objects.filter(id=self.kwargs.get('pk'))
                for i in pki:
                    pku = i.user_id
                if pku == request.user.id:
                    form = self.get_form()
                    data = form.save()
                else:
                    data['error'] = 'No tienes las credenciales correspondientes'
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar categoria'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit'
        context['url_link'] = self.success_url
        return context

class CategoriesDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Categories
    template_name = 'categories/delete.html'
    success_url = reverse_lazy('list_categories')
    permission_required = 'delete_categories'
    url_redirect = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pku = 0
            pki = Categories.objects.filter(id=self.kwargs.get('pk'))
            for i in pki:
                pku = i.user_id
            if pku == request.user.id:
                self.object.delete()
            else:
                data['error'] = 'No tienes los permisos correspondientes'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar categoria'
        context['icon'] = 'fa-trash-alt'
        context['url_link'] = self.success_url
        return context