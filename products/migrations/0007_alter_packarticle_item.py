# Generated by Django 3.2 on 2021-10-12 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20211012_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packarticle',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.article', verbose_name='Article'),
        ),
    ]
