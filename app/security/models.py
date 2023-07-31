from datetime import datetime
from crum import get_current_request
from django.db import models
from django.forms import model_to_dict
from security.choices import LOGIN_TYPE
from user.models import User
# Create your models here.
class AccessUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    ip_address = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=LOGIN_TYPE, default=LOGIN_TYPE[0][0])
    def __str__(self):
        return self.ip_address
    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['time_joined'] = self.time_joined.strftime('%H:%M:%S')
        return item
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        request = get_current_request()
        self.ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if not self.ip_address:
            self.ip_address = request.META.get('REMOTE_ADDR')
        super(AccessUsers, self).save()
    class Meta:
        verbose_name = 'Acceso de usuario'
        verbose_name_plural= 'Accesos de usuarios'
        ordering = ['-id']