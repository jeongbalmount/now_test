# Generated by Django 3.0.4 on 2020-04-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0035_auto_20200422_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='fps_value',
            field=models.IntegerField(default=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadurlmodel',
            name='url_fps_value',
            field=models.IntegerField(default=15),
            preserve_default=False,
        ),
    ]