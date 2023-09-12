from django.db import models
from django.contrib.auth.models import User


class Improvement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=560)
    status = models.CharField(max_length=50, choices=(
        ('enviado', 'enviado'),
        ('em análise', 'em análise'),
        ('em desenvolvimento', 'em desenvolvimento'),
        ('recusado', 'recusado'),
        ('concluído', 'concluído'),
    ))

    def __str__(self) -> str:
        return self.title
