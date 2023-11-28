# Generated by Django 4.2.4 on 2023-11-28 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0006_company_company_suffix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_suffix',
            field=models.CharField(blank=True, help_text='Enter your Company Suffix', max_length=10, null=True),
        ),
    ]