# Generated by Django 4.1.5 on 2023-08-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('brand', models.CharField(max_length=250)),
                ('image', models.URLField()),
                ('ingredients', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('products', models.ManyToManyField(to='product.product')),
            ],
        ),
    ]
