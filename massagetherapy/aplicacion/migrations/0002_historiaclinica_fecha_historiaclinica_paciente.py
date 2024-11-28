# Generated by Django 5.0.3 on 2024-06-24 23:57

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historiaclinica',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historiaclinica',
            name='paciente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aplicacion.usuario'),
            preserve_default=False,
        ),
    ]
