# Generated by Django 5.0.3 on 2024-10-10 02:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0004_alter_reserva_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
    ]
