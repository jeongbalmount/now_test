# Generated by Django 3.0.4 on 2020-05-20 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0042_auto_20200519_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadurlmodel',
            name='URL_fps_value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploadurlmodel',
            name='URL_scaleValue_select',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
