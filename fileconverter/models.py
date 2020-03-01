from urllib.parse import urlparse
from urllib.request import urlretrieve
from django.core.files import File
from django.db import models
from .utils.file import download


class UploadModel(models.Model):
    uploadedFile = models.FileField(upload_to='uploadedFiles/%Y/%m/%d/', blank=True)
    uploadByURL = models.URLField(max_length=350)

    def save(self, *args, **kwargs):
        # ImageField에 파일이 없고, url이 존재하는 경우에만 실행
        if self.uploadByURL and not self.uploadedFile:
            # 우선 purchase_url의 대표 이미지를 크롤링하는 로직은 생략하고, 크롤링 결과 이미지 url을 임의대로 설정
            item_image_url = self.uploadByURL

            if item_image_url:
                temp_file = download(item_image_url)
                file_name = '{urlparse}'.format(
                    # url의 마지막 '/' 내용 중 확장자 제거
                    # ex) url = 'https://~~~~~~/bag-1623898_960_720.jpg'
                    #     -> 'bag-1623898_960_720.jpg'
                    #     -> 'bag-1623898_960_720'
                    urlparse=urlparse(item_image_url).path.split('/')[-1].split('.')[0],
                )
                self.uploadedFile.save(file_name, File(temp_file))
                super().save()
            else:
                super().save()

    def __str__(self):
        return self.uploadedFile.name