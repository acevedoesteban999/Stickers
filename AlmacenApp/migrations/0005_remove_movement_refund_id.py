# Generated by Django 4.1.7 on 2023-02-19 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlmacenApp', '0004_alter_movement_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movement',
            name='refund_id',
        ),
    ]
