# Generated by Django 4.1.7 on 2023-02-20 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AlmacenApp', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]