# Generated by Django 2.2 on 2020-03-06 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0006_auto_20200306_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='uploadFileFirst',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='uploadmodel',
            name='uploadFileSecond',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]