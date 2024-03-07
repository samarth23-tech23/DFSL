# Generated by Django 5.0.2 on 2024-02-17 08:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0007_alter_warrantyclaim_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warrantyclaim',
            name='price_with_gst',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
