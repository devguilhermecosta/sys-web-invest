# Generated by Django 4.2.1 on 2023-08-14 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_remove_fiihistory_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='cnpj',
            field=models.CharField(max_length=18),
        ),
        migrations.AlterField(
            model_name='action',
            name='code',
            field=models.CharField(max_length=5),
        ),
    ]