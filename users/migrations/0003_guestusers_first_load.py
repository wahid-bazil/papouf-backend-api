# Generated by Django 3.2 on 2021-10-12 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211012_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestusers',
            name='first_load',
            field=models.BooleanField(default=True),
        ),
    ]
