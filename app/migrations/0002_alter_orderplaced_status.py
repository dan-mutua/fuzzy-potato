# Generated by Django 4.1.4 on 2022-12-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the Way', 'On the Way'), ('Delivered', 'Delevered'), ('Cancel', 'Cancel')], default='Pending', max_length=50),
        ),
    ]
