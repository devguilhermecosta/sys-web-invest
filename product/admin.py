from django.contrib import admin
from .models import UserAction


@admin.register(UserAction)
class UserAction(admin.ModelAdmin):
    ...
