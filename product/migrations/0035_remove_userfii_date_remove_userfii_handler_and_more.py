# Generated by Django 4.2.1 on 2023-08-11 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_remove_useraction_date_remove_useraction_handler_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfii',
            name='date',
        ),
        migrations.RemoveField(
            model_name='userfii',
            name='handler',
        ),
        migrations.RemoveField(
            model_name='userfii',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='userfii',
            name='unit_price',
        ),
    ]
