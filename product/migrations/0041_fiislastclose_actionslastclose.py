# Generated by Django 4.2.1 on 2023-08-24 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_alter_action_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIIsLastClose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_close', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fii', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.fii')),
            ],
        ),
        migrations.CreateModel(
            name='ActionsLastClose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_close', models.DecimalField(decimal_places=2, max_digits=15)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.action')),
            ],
        ),
    ]
