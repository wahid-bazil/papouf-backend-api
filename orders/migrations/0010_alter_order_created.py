# Generated by Django 3.2 on 2021-10-12 09:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 9, 10, 47, 704456, tzinfo=utc)),
        ),
    ]