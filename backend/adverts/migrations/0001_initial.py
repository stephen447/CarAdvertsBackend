# Generated by Django 5.0 on 2024-08-25 16:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('make', models.CharField(max_length=50, verbose_name='Make')),
                ('model', models.CharField(max_length=50, verbose_name='Model')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('mileage', models.PositiveIntegerField(verbose_name='Mileage (in miles)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('fuel_type', models.CharField(max_length=20, verbose_name='Fuel Type')),
                ('transmission', models.CharField(max_length=20, verbose_name='Transmission')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('condition', models.CharField(max_length=30, verbose_name='Condition')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Updated At')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Seller')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdvertisementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_data', models.BinaryField()),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='adverts.advert')),
            ],
        ),
    ]
