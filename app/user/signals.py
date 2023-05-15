from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import  post_save
from user.models import User

@receiver(post_save, sender=User)
def addUserGroup(sender, instance, created, **kwargs):
    if created:
        try:
            students = Group.objects.get(name='Administrador')
        except Group.DoesNotExist:
            students = Group.objects.create(name='Administrador')
        instance.User.groups.add(students)