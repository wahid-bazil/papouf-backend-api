# Generated by Django 3.2 on 2021-10-12 12:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 12, 13, 6, 471920, tzinfo=utc)),
        ),
    ]
