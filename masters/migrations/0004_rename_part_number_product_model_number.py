# Generated by Django 4.2.4 on 2023-10-28 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0003_product_amc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='part_number',
            new_name='model_number',
        ),
    ]
