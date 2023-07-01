# Generated by Django 4.2.1 on 2023-07-01 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_fiis_fii_alter_actionhistory_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfii',
            name='date',
            field=models.DateField(default='2023-07-01'),
        ),
        migrations.AddField(
            model_name='userfii',
            name='handler',
            field=models.CharField(default='buy', max_length=255),
        ),
        migrations.AlterField(
            model_name='actionhistory',
            name='date',
            field=models.DateField(default='2023-07-01'),
        ),
        migrations.AlterField(
            model_name='useraction',
            name='date',
            field=models.DateField(default='2023-07-01'),
        ),
        migrations.CreateModel(
            name='FiiHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handler', models.CharField(choices=[('B', 'buy'), ('S', 'sell'), ('P', 'proceeds')], max_length=255)),
                ('date', models.DateField(default='2023-07-01')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('trading_note', models.FileField(blank=True, null=True, upload_to='trading-notes/fiis/')),
                ('useraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.userfii')),
            ],
        ),
    ]
