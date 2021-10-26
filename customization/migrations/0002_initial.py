# Generated by Django 3.2 on 2021-10-11 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('products', '0001_initial'),
        ('customization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompack',
            name='device_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.guestusers'),
        ),
        migrations.AddField(
            model_name='custompack',
            name='items',
            field=models.ManyToManyField(through='customization.CustomPackArticle', to='products.Article'),
        ),
        migrations.AddField(
            model_name='custompack',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
