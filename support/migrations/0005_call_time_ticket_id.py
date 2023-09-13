# Generated by Django 4.2.4 on 2023-09-12 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_rename_overview_ticket_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='call_time',
            name='ticket_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_call_times', to='support.ticket'),
        ),
    ]
