# Generated by Django 5.0.3 on 2024-10-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0009_reserva_fecha_reserva_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='hora',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
