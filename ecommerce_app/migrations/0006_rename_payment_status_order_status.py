# Generated by Django 4.2 on 2023-12-14 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0005_order_payment_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_status',
            new_name='status',
        ),
    ]