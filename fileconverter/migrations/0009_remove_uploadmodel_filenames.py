# Generated by Django 2.2 on 2020-03-08 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0008_auto_20200306_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadmodel',
            name='fileNames',
        ),
    ]