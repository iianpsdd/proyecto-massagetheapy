# Generated by Django 5.0.3 on 2024-10-15 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0005_usuario_fecha_nacimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
