from django.contrib import admin

from user.models import User


# Register your models here.

@admin.register(User)
class PeliculaAdmin(admin.ModelAdmin):
    pass