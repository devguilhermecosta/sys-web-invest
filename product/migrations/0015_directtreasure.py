# Generated by Django 4.2.1 on 2023-07-14 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0014_rename_fixedinomehistory_fixedincomehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectTreasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('selic', 'selic'), ('ipca', 'ipca'), ('prefixado', 'prefixado')], max_length=255)),
                ('interest_receipt', models.CharField(choices=[('não há', 'não há'), ('mensal', 'mensal'), ('trimestral', 'trimestral'), ('semestral', 'semestral'), ('anual', 'anual')], max_length=255)),
                ('profitability', models.CharField(max_length=255)),
                ('maturity_date', models.DateField(default='2023-07-02')),
                ('value', models.FloatField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
