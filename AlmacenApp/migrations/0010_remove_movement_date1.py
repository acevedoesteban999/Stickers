# Generated by Django 4.1.7 on 2023-02-20 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlmacenApp', '0009_movement_date1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movement',
            name='date1',
        ),
    ]