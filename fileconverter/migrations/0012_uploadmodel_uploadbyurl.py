# Generated by Django 2.2 on 2020-03-13 06:01

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0011_auto_20200312_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='uploadByURL',
            field=models.TextField(default=django.utils.timezone.now, validators=[django.core.validators.URLValidator()]),
            preserve_default=False,
        ),
    ]