from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from crum import get_current_request
class ValidatePermissionRequiredMinxin(object):
    permission_required = ''
    url_redirect = None
    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('inicio')
        return self.url_redirect
    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if 'group' in request.session:
            group = request.session['group']
            perms = self.get_perms()
            if group.permissions.filter(codename__in=perms):
                return super().dispatch(request, *args, **kwargs)
        messages.error(request, f'El usuario {request.user.first_name} {request.user.last_name} con el perfil de {group.name} No tiene los permisos para ingresar a este modulo')
        return HttpResponseRedirect(self.get_url_redirect())