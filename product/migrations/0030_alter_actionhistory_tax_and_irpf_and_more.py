# Generated by Django 4.2.1 on 2023-08-04 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_alter_fixedincomehistory_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionhistory',
            name='tax_and_irpf',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='actionhistory',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='actionhistory',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='directtreasure',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='directtreasurehistory',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='fiihistory',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='fiihistory',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]