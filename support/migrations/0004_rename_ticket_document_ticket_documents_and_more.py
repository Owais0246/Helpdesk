# Generated by Django 4.2.4 on 2023-09-04 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_ticket_location_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='ticket_document',
            new_name='documents',
        ),
        migrations.RemoveField(
            model_name='document',
            name='ticket',
        ),
    ]
