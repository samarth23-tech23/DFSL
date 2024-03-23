# Generated by Django 5.0.2 on 2024-02-26 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_no', models.CharField(max_length=255)),
                ('lab_name', models.CharField(max_length=255)),
                ('letter_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.letter')),
            ],
        ),
        migrations.CreateModel(
            name='Subproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_part', models.CharField(max_length=255)),
                ('part_name', models.CharField(max_length=255)),
                ('specification', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('buying_date', models.DateField()),
                ('price_of_item', models.DecimalField(decimal_places=2, max_digits=10)),
                ('period_of_amc_contract', models.CharField(max_length=255)),
                ('amc_provider', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='letterCreation.product')),
            ],
        ),
    ]