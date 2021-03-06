# Generated by Django 3.2 on 2021-10-11 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_Mode',
            fields=[
                ('title', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('shipping_total_price', models.DecimalField(decimal_places=2, default=5.99, max_digits=50)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='IntervalOrderToltal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_total', models.FloatField()),
                ('max_total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShippingBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('max_width', models.FloatField()),
                ('max_length', models.FloatField()),
                ('max_heigth', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShippingBoxGroupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('max_volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShippingCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_shipping_min_total', models.FloatField()),
                ('free_shipping_max_total', models.FloatField()),
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('slug', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingNetPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net_shipping_price', models.FloatField()),
                ('cities', models.ManyToManyField(to='delivery.ShippingCity')),
                ('shipping_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.shippingmode')),
                ('total_order_interval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.intervalordertoltal')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDelay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delay_per_hour', models.PositiveIntegerField()),
                ('cities', models.ManyToManyField(to='delivery.ShippingCity')),
                ('shipping_mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.shippingmode')),
            ],
        ),
        migrations.AddField(
            model_name='shippingcity',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='delivery.shippingregion'),
        ),
        migrations.AddField(
            model_name='intervalordertoltal',
            name='shipping_mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.shippingmode'),
        ),
    ]
