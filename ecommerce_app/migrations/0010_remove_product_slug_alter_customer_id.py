# Generated by Django 4.2 on 2023-12-15 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0009_product_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]