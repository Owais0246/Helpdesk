# Generated by Django 4.2.4 on 2024-01-12 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0014_remove_ticket_spare_cost_sparecost_ticket_spare_cost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='call_time',
            options={'ordering': ['schedule']},
        ),
    ]