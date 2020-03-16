from io import BytesIO
from os import path
from django.core.validators import URLValidator
from django import forms
from django.core.files import File
from requests import get

from .models import UploadModel, UploadURLmodel
import filetype


class UploadFileForm(forms.ModelForm):
    max_size = 52428800
    videoTypes = ['video/x-m4v', 'video/x-matroska', 'video/webm', 'video/quicktime',
                  'video/x-msvideo', 'video/x-ms-wmv', 'video/mpeg', 'video/x-flv', 'video/mp4']

    class Meta:
        model = UploadModel
        fields = ['uploadedFiles', ]

    def clean_uploadedFiles(self):
        uploadFiles = self.cleaned_data['uploadedFiles']
        uploadFileList = self.files.getlist('uploadedFiles')
        AllfileSize = 0

        if len(uploadFileList) > 2 :
            raise forms.ValidationError('파일이 2개 이상입니다.')
        print("len")
        for filesize in uploadFileList:
            AllfileSize = filesize.size
            print(filesize.size)
        # 50MB를 넘었을때
        if AllfileSize > self.max_size:
            print('파일 크기')
            raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

        for file in uploadFileList:
            # print(file)
            checkfile = filetype.guess(file)
            print(checkfile.mime)

            # 비디오 파일이 아닐시
            if checkfile.mime not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')


            print('File extension: %s' % checkfile.extension)
            print('File MIME type: %s' % checkfile.mime)
        print(uploadFileList)

        return uploadFiles


class UploadURLForm(forms.ModelForm):
    class Meta:
        model = UploadURLmodel
        fields = ['uploadURL', 'fileFromURL']
        videoTypes = ['avi', 'flv', 'wmv', 'mov', 'mp4','webm']

    def save(self, *args, **kwargs):
        print("save me")
        uploadURL = self.cleaned_data['uploadURL']
        fileFromURL = self.cleaned_data['fileFromURL']
        # 파일 url 받아서 파싱한 후 저장
        if uploadURL and not self.fileFromURL:
            file_url = uploadURL
            furl, file_extension = path.splitext(file_url)

            if URLValidator(file_url) == False and file_extension not in self.videoTypes:
                raise forms.ValidationError('정확한 url형식을 적어주세요')

            file_name = file_url.split('/')[-1]

            response = get(file_url)
            binary_data = response.content
            temp_file = BytesIO()
            temp_file.write(binary_data)
            temp_file.seek(0)
            print(File(temp_file))
            print("wow")
            fileFromURL.save(
                file_name,
                File(temp_file)
            )
            print(self.uploadedFiles)
        super(UploadURLForm, self).save()

