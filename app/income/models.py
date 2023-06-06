from datetime import datetime
import uuid
from crum import get_current_user, get_current_request
from django.db import models
from django.forms import model_to_dict
from categories.models import Categories
from user.models import User
from app.settings import *
# Create your models here.
OPCIONES = (
    ('Esperando a recibir', 'Esperando a recibir'),
    ('Ya ha sido recibido', 'Ya ha sido recibido')
)
class Income(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descripción')
    amount = models.DecimalField(max_digits=15, decimal_places=2,  verbose_name='Monto')
    iva = models.DecimalField(max_digits=5, decimal_places=2,  verbose_name='Iva')
    totaliva = models.DecimalField(max_digits=20, decimal_places=2,  verbose_name='Total Iva')
    total = models.DecimalField(max_digits=20, decimal_places=2,  verbose_name='Total')
    image = models.ImageField(upload_to='factures/%Y/%m/%d', null=True, blank=True, verbose_name='Fatura')
    state = models.CharField(max_length=50, choices=OPCIONES, verbose_name='Estado')
    date_joined = models.DateField(editable=True, default=datetime.now)
    annotations = models.CharField(max_length=255, verbose_name='Anotaciones', null=True, blank=True)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='categorias')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income',)
    def __str__(self):
        return self.description
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    def save(self, *args, **kwargs):
        request = get_current_request()
        if not self.user_id:
            self.user_id = request.user.id
        super().save(*args, **kwargs)
    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        return item
    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
        db_table = 'tb_Incomes'
        ordering = ['-id']