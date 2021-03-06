# Generated by Django 3.2 on 2021-10-28 09:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20211028_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderemail',
            name='order_status',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_id',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_is_paid',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_orderSubtotal',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_paymentMode',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_shippingAddress',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_shippingCost',
        ),
        migrations.RemoveField(
            model_name='orderemail',
            name='send_shippingMode',
        ),
        migrations.AddField(
            model_name='orderemail',
            name='status',
            field=models.CharField(choices=[('created', 'Préparation pour la livraison'), ('shipping', 'En cours de livraison'), ('shipped', 'Livrée'), ('refunded', 'Retournéé')], default='created', max_length=120),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 28, 9, 37, 25, 100248, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='orderemail',
            name='text',
            field=models.TextField(blank=True, max_length=500, verbose_name='subject'),
        ),
    ]
