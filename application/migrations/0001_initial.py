# Generated by Django 4.2.2 on 2023-06-27 02:32

import application.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(editable=False, max_length=50, unique=True)),
                ('name', models.CharField(help_text='Enter Brand Name', max_length=50, unique=True, verbose_name='Brand Name')),
                ('isnotpopular', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(editable=False, max_length=50, unique=True)),
                ('name', models.CharField(help_text='Enter Category Name', max_length=50, unique=True, verbose_name='Category Name')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('data', models.CharField(editable=False, max_length=50, unique=True)),
                ('name', models.CharField(help_text='Enter Device Name', max_length=50, unique=True, verbose_name='Device Name')),
                ('active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('processsed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(editable=False, max_length=50, unique=True)),
                ('title', models.CharField(editable=False, max_length=255, unique=True)),
                ('stock', models.SmallIntegerField(default=0)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('code', models.CharField(blank=True, editable=False, max_length=15, null=True, unique=True)),
                ('image', models.ImageField(blank=True, editable=False, help_text='Select image file to upload', max_length=250, null=True, upload_to=application.models.upload_to, verbose_name='Product Image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.category')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.device')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.SmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='application.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='application.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
