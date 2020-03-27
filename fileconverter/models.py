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
    uploadURL = models.URLField(blank=False)
    fileFromURL = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        # 파일 url 받아서 파싱한 후 저장
        print("in model")
        if self.uploadURL and not self.fileFromURL:
            print("uploadURK")
            super().save(*args, **kwargs)
            file_url = self.uploadURL

            file_name = file_url.split('/')[-1]

            response = get(file_url)
            binary_data = response.content
            temp_file = BytesIO()
            temp_file.write(binary_data)
            temp_file.seek(0)
            print("파일 저장")
            # fileField에 들어 있는 save(name, content, safe?)메소드 사용
            self.fileFromURL.save(
                file_name,
                File(temp_file)
            )
            print("return from save")
            print(self.fileFromURL.name)
            return self.fileFromURL.name

        # print("else")
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.fileFromURL.name


class CheckFileType(models.Model):
    checkType = models.BooleanField(blank=False)

