# Generated by Django 3.2.16 on 2022-10-28 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20221028_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='seller_id',
            field=models.IntegerField(),
        ),
    ]
