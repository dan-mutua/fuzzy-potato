# Generated by Django 4.1.4 on 2023-07-25 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_customer_state_remove_product_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_purchased',
            field=models.BooleanField(default=False),
        ),
    ]