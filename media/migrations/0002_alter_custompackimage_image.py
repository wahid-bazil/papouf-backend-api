# Generated by Django 3.2 on 2021-08-25 16:26

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompackimage',
            name='image',
            field=models.ImageField(default='posts/default.jpg', upload_to=media.models.upload_to, verbose_name='Image'),
        ),
    ]