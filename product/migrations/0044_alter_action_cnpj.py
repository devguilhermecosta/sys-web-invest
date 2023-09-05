# Generated by Django 4.2.1 on 2023-09-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_fii_last_close'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='cnpj',
            field=models.CharField(blank=True, default='', error_messages={'unique': 'Este CNPJ já está em uso'}, max_length=18, null=True, unique=True),
        ),
    ]