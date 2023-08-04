import smtplib
import uuid
from django.contrib import messages
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import settings
from django.contrib.auth.mixins import *
from django.http import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from locked.forms import ActivateForm, ChangeActivateUserForm
from security.models import AccessUsers
from user.mixins import ValidatePermissionRequiredMinxin
from user.models import User
# Create your views here.
class LockedListView(LoginRequiredMixin, ValidatePermissionRequiredMinxin, TemplateView):
    template_name = 'locked/list.html'
    permission_required = 'view_user'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
          action = request.POST['action']
          if action == 'searchdata':
              data = []
              position = 1
              for i in User.objects.filter(is_active=False):
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
        context['title'] = 'Lista de usuarios inhabilitados'
        context['icon'] = 'fa-list mr-1'
        context['url_link'] = reverse_lazy('list_locked')
        context['create_url'] = reverse_lazy('activate_locked')
        return context
class LockedActivateFormView(LoginRequiredMixin, ValidatePermissionRequiredMinxin,FormView):
    form_class = ActivateForm
    template_name = 'locked/activate.html'
    success_url = reverse_lazy('list_locked')
    permission_required = 'add_user'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        users_inactive = User.objects.filter(is_active=False).exists()
        if not users_inactive:
            messages.error(request, 'No hay usuarios inactivos.')
            return HttpResponseRedirect(reverse_lazy('list_locked'))
        return super().dispatch(request, *args, **kwargs)
    def send_email_reset_password(self, user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Habilitar cuenta'

            content = render_to_string('activate_user.html', {
                'user': user,
                'link_resetpwd': 'http://{}/activate/account/user/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(
                settings.EMAIL_HOST_USER,
                email_to,
                mensaje.as_string()
            )
            print('exito')
        except Exception as e:
            data['error'] = str(e)
        return data

    def get_last_login(self, username):
        user = User.objects.get(username=username)
        if user.last_login is None:
            print('hola last login')
            user.last_login = datetime.now()
            user.save()
        return user.toJSON()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ActivateForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    queryset = User.objects.filter(username=username)
                    if queryset.exists():
                       user = form.get_user()
                       data = {
                           'data': self.send_email_reset_password(user),
                           'success': user.email
                       }
                else:
                    data['error'] = form.errors
            elif action == 'autocomplete':
                data = []
                for i in User.objects.filter(username__icontains=request.POST['term'], is_active=False)[0:10]:
                    # item
                    item = self.get_last_login(i.username)
                    item['value'] = i.username
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Habilitar usuario'
        context['icon'] = 'fa-user-check mr-1'
        context['action'] = 'add'
        context['url_link'] = self.success_url
        return context
class ChangeActivateUserView(LoginRequiredMixin, ValidatePermissionRequiredMinxin,FormView):
    form_class = ChangeActivateUserForm
    template_name = 'locked/activateuser.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangeActivateUserForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                user = User.objects.get(token=self.kwargs['token'])
                if username == user.username:
                    acess = AccessUsers.objects.filter(user_id=user.pk)
                    for ac in acess:
                        a = AccessUsers.objects.get(id=ac.id)
                        a.delete()
                    user.set_password(request.POST['password'])
                    user.token = uuid.uuid4()
                    user.is_active = True
                    user.save()
                else:
                    data['error'] = 'El usuario no exixte'
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        return context