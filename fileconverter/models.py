from io import BytesIO
from django.core.files import File
from django.db import models
from django.shortcuts import reverse


class UploadModel(models.Model):
    first_uploaded_file = models.FileField(blank=False, upload_to='first/%Y/%m/%d/')
    second_uploaded_file = models.FileField(blank=True, upload_to='second/%Y/%m/%d/')
    scaleValue_select_1 = models.CharField(blank=False, max_length=15)
    scaleValue_select_2 = models.CharField(blank=True, null=True, max_length=15)
    fps_value_1 = models.IntegerField(blank=False)
    fps_value_2 = models.IntegerField(blank=True, null=True)
    start_1 = models.FloatField(blank=False, null=False)
    start_2 = models.FloatField(blank=True, null=True)
    end_1 = models.FloatField(blank=False, null=False)
    end_2 = models.FloatField(blank=True, null=True)
    use_palette_1 = models.IntegerField(blank=False)
    use_palette_2 = models.IntegerField(blank=True, null=True)


class UploadURLmodel(models.Model):
    uploadURL_1 = models.URLField(blank=False, null=False)
    uploadURL_2 = models.URLField(blank=True, null=True)
    URL_fps_value_1 = models.IntegerField(blank=False, null=False)
    URL_fps_value_2 = models.IntegerField(blank=True, null=True)
    URL_scaleValue_select_1 = models.CharField(blank=False, null=False, max_length=20)
    URL_scaleValue_select_2 = models.CharField(blank=True, null=True, max_length=20)
    URL_start_1 = models.FloatField(blank=False, null=False)
    URL_start_2 = models.FloatField(blank=True, null=True)
    URL_end_1 = models.FloatField(blank=False, null=False)
    URL_end_2 = models.FloatField(blank=True, null=True)
    use_palette_1 = models.IntegerField(blank=False, null=False)
    use_palette_2 = models.IntegerField(blank=True, null=True)









