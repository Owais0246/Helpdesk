# Generated by Django 4.2.4 on 2024-01-24 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0015_alter_call_time_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='sales_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_person', to=settings.AUTH_USER_MODEL),
        ),
    ]
