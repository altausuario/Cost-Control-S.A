from crum import get_current_user, get_current_request
from django.db import models
from django.forms import model_to_dict
from categories.models import Categories
from user.models import User

# Create your models here.
OPCIONES = (
    ('Esperando a recibir', 'Esperando a recibir'),
    ('Ya ha sido recibido', 'Ya ha sido recibido')
)
class Income(models.Model):
    description = models.CharField(max_length=255, verbose_name='Descripción')
    amount = models.DecimalField(max_digits=15, decimal_places=2,  verbose_name='Monto')
    state = models.CharField(max_length=50, choices=OPCIONES, verbose_name='Estado')
    date_creation = models.DateTimeField(verbose_name='Fecha del ingreso', editable=True)
    annotations = models.CharField(max_length=255, verbose_name='Anotaciones', null=True, blank=True)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='categorias')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income',)
    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        request = get_current_request()
        if not self.user_id:
            self.user_id = request.user.id
        super().save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_creation'] = self.date_creation.strftime('%Y-%m-%d %H:%m')
        return item
    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
        db_table = 'tb_Incomes'
        ordering = ['-id']