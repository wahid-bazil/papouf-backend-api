# Generated by Django 3.2 on 2021-10-11 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20211012_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pack',
            options={'ordering': ['-orders'], 'verbose_name': 'pack'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-orders'], 'verbose_name': 'product'},
        ),
    ]
