from io import BytesIO
from django.core.files import File
from django.core.validators import URLValidator
from django.db import models
from requests import get


class UploadModel(models.Model):
    uploadedFiles = models.FileField(blank=True,)
    def __str__(self):
        return self.uploadedFiles.name


class UploadURLmodel(models.Model):
    uploadURL = models.TextField(blank=False)
    fileFromURL = models.ForeignKey(UploadModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.fileFromURL.name