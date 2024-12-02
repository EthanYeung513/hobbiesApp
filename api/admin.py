from django.contrib import admin
from .models import AppUser, Hobby

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Hobby)