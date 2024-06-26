# Generated by Django 4.2.1 on 2023-08-04 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_remove_productfixedincome_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedincomehistory',
            name='state',
            field=models.CharField(default='apply', max_length=255),
        ),
        migrations.AlterField(
            model_name='productfixedincome',
            name='grace_period',
            field=models.DateField(default=''),
        ),
        migrations.AlterField(
            model_name='productfixedincome',
            name='maturity_date',
            field=models.DateField(default=''),
        ),
    ]
