# Generated by Django 5.0.3 on 2024-10-18 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0007_alter_usuario_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.usuario'),
        ),
    ]