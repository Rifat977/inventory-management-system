# Generated by Django 3.2.16 on 2022-10-28 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_cart_seller_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='seller_id',
            field=models.IntegerField(),
        ),
    ]
