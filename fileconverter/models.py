from io import BytesIO
from django.core.files import File
from django.db import models
from requests import get


class UploadModel(models.Model):
    first_uploaded_file = models.FileField(blank=False, upload_to='first/%Y/%m/%d/')
    second_uploaded_file = models.FileField(blank=True, upload_to='second/%Y/%m/%d/')
    fps_value_1 = models.IntegerField(blank=False)
    fps_value_2 = models.IntegerField(blank=True)


class UploadURLmodel(models.Model):
    uploadURL = models.URLField(blank=False)
    fileFromURL = models.FileField(blank=True, upload_to='urlmedia/%Y/%m/%d/')

    def save(self, *args, **kwargs):
        # 파일 url 받아서 파싱한 후 저장
        print("in model")
        if self.uploadURL and not self.fileFromURL:
            print("uploadURL")
            super().save(*args, **kwargs)
            file_url = self.uploadURL
            print(file_url)
            file_name = file_url.split('/')[-1]
            print(file_name)
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
            print(self.fileFromURL.name + " url이름")
            return self.fileFromURL.name

        # print("else")
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.fileFromURL.name




