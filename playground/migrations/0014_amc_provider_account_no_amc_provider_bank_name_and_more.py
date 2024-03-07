# Generated by Django 5.0.2 on 2024-02-21 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0013_remove_item_department_remove_item_lab_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='amc_provider',
            name='account_no',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='amc_provider',
            name='bank_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='amc_provider',
            name='branch',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='amc_provider',
            name='ifsc_code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='amc_provider',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
