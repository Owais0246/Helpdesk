# Generated by Django 4.2.4 on 2023-10-07 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('start_date', models.DateField()),
                ('expiry', models.DateField(blank=True, null=True)),
                ('sla', models.TextField(max_length=1000)),
                ('escalation_matrix_1', models.TextField(max_length=1000)),
                ('escalation_matrix_2', models.TextField(max_length=1000)),
                ('escalation_matrix_3', models.TextField(max_length=1000)),
                ('escalation_matrix_4', models.TextField(max_length=1000)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masters.company')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masters.location')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='masters.product')),
            ],
        ),
    ]
