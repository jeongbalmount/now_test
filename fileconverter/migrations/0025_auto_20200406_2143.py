# Generated by Django 3.0.4 on 2020-04-06 12:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fileconverter', '0024_checkfiletype'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkfiletype',
            name='fileName',
            field=models.CharField(default=django.utils.timezone.now, max_length=70),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadmodel',
            name='uploadedFiles',
            field=models.FileField(blank=True, upload_to='filemedia/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='uploadurlmodel',
            name='fileFromURL',
            field=models.FileField(blank=True, upload_to='urlmedia/%Y/%m/%d/'),
        ),
    ]