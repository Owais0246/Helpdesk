# Generated by Django 4.2.4 on 2024-11-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0003_region_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='pin',
            field=models.IntegerField(),
        ),
    ]
