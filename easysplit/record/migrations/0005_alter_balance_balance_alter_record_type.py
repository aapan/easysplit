# Generated by Django 4.0.4 on 2023-06-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0004_alter_balance_balance_alter_from_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='balance',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='type',
            field=models.CharField(choices=[('expense', 'expense'), ('income', 'income'), ('transfer', 'transfer')], max_length=10),
        ),
    ]
