# Generated by Django 4.2.1 on 2023-08-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_alter_actionhistory_tax_and_irpf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directtreasure',
            name='value',
        ),
        migrations.AlterField(
            model_name='directtreasurehistory',
            name='tax_and_irpf',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]
