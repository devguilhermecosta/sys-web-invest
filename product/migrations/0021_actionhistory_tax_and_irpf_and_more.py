# Generated by Django 4.2.1 on 2023-07-30 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_remove_userfii_earnings_accumulated'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionhistory',
            name='tax_and_irpf',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actionhistory',
            name='handler',
            field=models.CharField(choices=[('B', 'buy'), ('S', 'sell'), ('D', 'dividends'), ('J', 'jscp'), ('R', 'remuneration'), ('rnt', 'renting')], max_length=255),
        ),
    ]