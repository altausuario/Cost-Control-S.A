from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from budget.models import *
from categories.forms import CategoriesForm
from categories.models import Categories
from income.forms import IncomeForm
from income.models import Income
from user.mixins import ValidatePermissionRequiredMinxin
# Create your views here.
class IncomeListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, ListView):
    model = Income
    template_name = 'income/list.html'
    permission_required = 'view_income'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_name_categories(self, pk):
        cat = Categories.objects.get(pk=pk.id)
        return cat.name
    def post(self, request, *args, **kwargs):
        data = []
        try:
          action = request.POST['action']
          if action == 'searchdata':
              position = 1
              for i in Income.objects.filter(user_id=request.user.id).order_by('id'):
                  item = i.toJSON()
                  item['position'] = position
                  name = self.get_name_categories(i.categorie)
                  item['categorie'] = name
                  data.append(item)
                  position += 1
          else:
              data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ingresos'
        context['icon'] = 'fa-bars-staggered mr-2'
        context['url_link'] = reverse_lazy('budget')
        context['create_url'] = reverse_lazy('create_income')
        return context
class IncomeCreateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/create.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'add_income'
    url_redirect = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_conversor(self, amount):
        print(amount)
        # valor_convertido = float(amount.replace("$ ", "").replace(".", "").replace(".", ","))
        valor_convertido = float(amount.replace("$", "").replace("\xa0", "").replace(".", "").replace(",", "."))
        print(valor_convertido)
        return valor_convertido
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                i = Income()
                i.id = kwargs.get('pk')
                i.description = request.POST['description']
                i.amount = self.get_conversor(request.POST['amount'])
                i.iva = request.POST['iva']
                i.totaliva = self.get_conversor(request.POST['totaliva'])
                i.total = self.get_conversor(request.POST['total'])
                i.image = request.POST['image']
                i.state = request.POST['state']
                i.date_joined = request.POST['date_joined']
                i.annotations = request.POST['annotations']
                i.categorie_id = request.POST['categorie']
                i.save()
            elif action == 'search_categories':
                data = []
                categories = Categories.objects.filter(name__icontains=request.POST['term'])[0:10]
                for cat in categories:
                    item = cat.toJSON()
                    item['text'] = cat.name
                    data.append(item)
                print(data)
            elif action == 'create_categories':
                with transaction.atomic():
                    frmCategories = CategoriesForm(request.POST)
                    data = frmCategories.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo ingreso'
        context['action'] = 'add'
        context['icon'] = 'fa-plus mr-2'
        context['img'] = 'facture.png'
        context['url_link'] = self.success_url
        context['cat'] = CategoriesForm
        return context
class IncomeUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/create.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'change_income'
    url_redirect = reverse_lazy('inicio')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def get_calcular(self):
        budget = Budget.objects.all().order_by('id')
        total_ex = 0
        total_in = 0
        total = 0
        for b in budget:
            exc = ExpensesConetion.objects.filter(budget_id=b.id)
            for ec in exc:
                ex = Expenses.objects.filter(id=ec.expenses_id)
                for e in ex:
                    total_ex += e.total
            inc = IncomeConetion.objects.filter(budget_id=b.id)
            for inm in inc:
                ino = Income.objects.filter(id=inm.income_id)
                for i in ino:
                    total_in += i.total
            total = total_in - total_ex
            but =Budget()
            but.id = b.id
            but.name = b.name
            but.date_joined = b.date_joined
            but.total_income = total_in
            but.total_expenses = total_ex
            but.total = total
            but.save()
            total_ex = 0
            total_in = 0
        return ''
    def image_income(self, pk):
        income = Income.objects.get(pk=pk)
        if not income.image:
            return 'facture.png'
        return income.image
    def get_conversor(self, amount):
        print(amount)
        # valor_convertido = float(amount.replace("$ ", "").replace(".", "").replace(".", ","))
        valor_convertido = float(amount.replace("$", "").replace("\xa0", "").replace(".", "").replace(",", "."))
        print(valor_convertido)
        return valor_convertido
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                pku = 0
                pki = Income.objects.filter(id=self.kwargs.get('pk'))
                for i in pki:
                    pku = i.user_id
                if pku == request.user.id:
                    i = Income()
                    i.id = kwargs.get('pk')
                    i.description = request.POST['description']
                    i.amount = self.get_conversor(request.POST['amount'])
                    i.iva = request.POST['iva']
                    i.totaliva = self.get_conversor(request.POST['totaliva'])
                    i.total = self.get_conversor(request.POST['total'])
                    i.image = request.POST['image']
                    i.state = request.POST['state']
                    i.date_joined = request.POST['date_joined']
                    i.annotations = request.POST['annotations']
                    i.categorie_id = request.POST['categorie']
                    i.save()
                    self.get_calcular()
                else:
                    data['error'] = 'No tienes las credenciales correspondientes'
            elif action == 'search_categories':
                data = []
                categories = Categories.objects.filter(name__icontains=request.POST['term'])[0:10]
                for cat in categories:
                    item = cat.toJSON()
                    item['text'] = cat.name
                    data.append(item)
            elif action == 'create_categories':
                with transaction.atomic():
                    frmCategories = CategoriesForm(request.POST)
                    data = frmCategories.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['title'] = 'Editar ingreso'
        context['action'] = 'edit'
        context['icon'] = 'fa-edit mr-2'
        context['img'] = self.image_income(pk)
        context['url_link'] = self.success_url
        context['cat'] = CategoriesForm
        return context
class IncomeDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, DeleteView):
    model = Income
    template_name = 'income/delete.html'
    success_url = reverse_lazy('list_income')
    permission_required = 'delete_income'
    url_redirect = reverse_lazy('inicio')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('list_budget'))
        return super().dispatch(request, *args, **kwargs)
    def get_calcular(self):
        budget = Budget.objects.all().order_by('id')
        total_ex = 0
        total_in = 0
        total = 0
        for b in budget:
            exc = ExpensesConetion.objects.filter(budget_id=b.id)
            for ec in exc:
                ex = Expenses.objects.filter(id=ec.expenses_id)
                for e in ex:
                    total_ex += e.amount

            inc = IncomeConetion.objects.filter(budget_id=b.id)
            for inm in inc:
                ino = Income.objects.filter(id=inm.income_id)
                for i in ino:
                    total_in += i.amount
            total = total_in - total_ex
            but =Budget()
            but.id = b.id
            but.name = b.name
            but.date_joined = b.date_joined
            but.total_income = total_in
            but.total_expenses = total_ex
            but.total = total
            but.save()
            total_ex = 0
            total_in = 0
        return ''
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pku = 0
            pki = Income.objects.filter(id=self.kwargs.get('pk'))
            for i in pki:
                pku = i.user_id
            if pku == request.user.id:
                self.object.delete()
                self.get_calcular()
            else:
                data['error'] = 'No tienes los permisos correspondientes'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar ingreso'
        context['icon'] = 'fa-trash-alt mr-2'
        context['url_link'] = self.success_url
        return context