# Generated by Django 3.2 on 2021-10-12 11:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 11, 11, 26, 321425, tzinfo=utc)),
        ),
    ]
