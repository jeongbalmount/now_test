from io import BytesIO
from django.core.files import File
from django.core.validators import URLValidator
from django.db import models
from requests import get


class UploadModel(models.Model):
    uploadedFiles = models.FileField(blank=False,)
    # uploadFileSecond = models.FileField(blank=True)
    # fileNames = models.CharField(blank=False, max_length=200)
    # secondFileName = models.CharField(blank=True, max_length=200)
    # uploadedFile = models.FileField(upload_to='uploadedFiles/%Y/%m/%d/', blank=True)
    # uploadByURL = models.TextField(validators=[URLValidator()])

    # def save(self, *args, **kwargs):
    #     # 파일 url 받아서 파싱한 후 저장
    #     if self.uploadByURL and not self.uploadedFile:
    #         file_url = self.uploadByURL
    #
    #         file_name = file_url.split('/')[-1]
    #
    #         response = get(file_url)
    #         binary_data = response.content
    #         temp_file = BytesIO()
    #         temp_file.write(binary_data)
    #         temp_file.seek(0)
    #         print("wow")
    #         self.uploadedFile.save(
    #             file_name,
    #             File(temp_file)
    #         )
    #     super(UploadModel, self).save()

    def __str__(self):
        return self.uploadedFiles.name