# Generated by Django 4.2.1 on 2023-07-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_directtreasurehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfii',
            name='earnings_accumulated',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
