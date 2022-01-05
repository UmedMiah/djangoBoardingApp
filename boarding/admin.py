from django.contrib import admin
from .models import Products, UserAccess

# Register your models here.
admin.site.register(Products)
admin.site.register(UserAccess)
