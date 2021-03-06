# Generated by Django 3.2 on 2021-10-11 15:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(default='', max_length=150)),
                ('variant_description', models.CharField(blank=True, max_length=30, null=True)),
                ('space', models.IntegerField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='products.article')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
            ],
            options={
                'verbose_name': 'article',
                'ordering': ['sale_price'],
            },
        ),
        migrations.CreateModel(
            name='Boxe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('cost_price', models.IntegerField()),
                ('sale_price', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(default='', max_length=150)),
                ('space', models.IntegerField()),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
            ],
            options={
                'verbose_name': 'boxe',
            },
        ),
        migrations.CreateModel(
            name='ItemStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(default=1)),
                ('is_customized', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='', max_length=1500)),
                ('orders', models.PositiveBigIntegerField(default=0)),
                ('boxe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.boxe')),
            ],
            options={
                'verbose_name': 'pack',
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35)),
                ('inventory', models.IntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('promo_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('promo_percentage', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(default='', max_length=200)),
                ('promo', models.BooleanField(default=False)),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='providers.provider')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.itemstatus')),
            ],
            options={
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='PackArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.article')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.pack')),
            ],
        ),
        migrations.AddField(
            model_name='pack',
            name='items',
            field=models.ManyToManyField(through='products.PackArticle', to='products.Article'),
        ),
        migrations.AddField(
            model_name='pack',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.itemstatus'),
        ),
    ]
