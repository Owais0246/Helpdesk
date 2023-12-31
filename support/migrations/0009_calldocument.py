# Generated by Django 4.2.4 on 2023-11-29 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0008_alter_call_time_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('call_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='support.call_time')),
            ],
        ),
    ]
