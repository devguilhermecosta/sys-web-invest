from django.contrib import admin
from .models.actions import UserAction


@admin.register(UserAction)
class UserAction(admin.ModelAdmin):
    ...
