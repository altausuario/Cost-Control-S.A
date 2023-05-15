from crum import get_current_request
from django.db import models
from django.forms import model_to_dict

from user.models import User


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name')
    description = models.CharField(max_length=255, verbose_name='Description')
    date_creation = models.DateField(auto_now_add=True,verbose_name='Date of creation')
    date_update = models.DateField(auto_now=True, verbose_name='Date of uptate')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        request = get_current_request()
        if not self.user_id:
            self.user_id = request.user.id
        super().save(*args, **kwargs)

    def fecha_creation(self):
        if self.date_creation:
            return '{}'.format(self.date_creation.strftime('%Y-%m-%d'))
        return '{}'.format(self.date_creation.strftime('%Y-%m-%d'))
    def toJSON(self):
        item = model_to_dict(self)
        item['date_creation'] = self.fecha_creation()
        return item

    class Meta:
        db_table = 'tb_categories'
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'
        ordering = ['id']