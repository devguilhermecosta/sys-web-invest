# Generated by Django 4.2.1 on 2023-08-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_alter_action_cnpj_alter_action_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='cnpj',
            field=models.CharField(error_messages={'unique': 'Este CNPJ já está em uso'}, max_length=18, unique=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='code',
            field=models.CharField(error_messages={'unique': 'Este código já está em uso'}, max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='fii',
            name='cnpj',
            field=models.CharField(error_messages={'unique': 'Este CNPJ já está em uso'}, max_length=18, unique=True),
        ),
        migrations.AlterField(
            model_name='fii',
            name='code',
            field=models.CharField(error_messages={'unique': 'Este código já está em uso'}, max_length=6, unique=True),
        ),
    ]
