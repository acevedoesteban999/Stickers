# Generated by Django 4.1.6 on 2023-02-10 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlmacenApp', '0006_caja_alter_movimientos_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientos',
            name='importe',
            field=models.IntegerField(default=0),
        ),
    ]
