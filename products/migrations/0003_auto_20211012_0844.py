# Generated by Django 3.2 on 2021-10-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_pack_boxe'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='caption',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='caption',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
