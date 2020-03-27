from os import path
from django.core.validators import URLValidator
from django import forms

from .models import UploadModel, UploadURLmodel, CheckFileType



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

        for filesize in uploadFileList:
            AllfileSize = filesize.size
            print(filesize.size)
        # 50MB를 넘었을때
        if AllfileSize > self.max_size:
            print('파일 크기')
            raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

        for file in uploadFileList:
            checkfile = file.content_type

            # 비디오 파일이 아닐시
            if checkfile not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')

        print(uploadFileList)

        return uploadFiles


class UploadURLForm(forms.ModelForm):
    class Meta:
        model = UploadURLmodel
        fields = ['uploadURL', 'fileFromURL']
        videoTypes = ['avi', 'flv', 'wmv', 'mov', 'mp4','webm']

    def clean_uploadURL(self):
        print("this is form")
        uploadURL = self.cleaned_data['uploadURL']
        # 파일 url 받아서 파싱한 후 저장
        file_url = uploadURL
        furl, file_extension = path.splitext(file_url)
        if URLValidator(file_url) == False and file_extension not in self.videoTypes:
            print("raised")
            raise forms.ValidationError('정확한 url형식을 적어주세요')

        print("before return")
        return uploadURL


class CheckTypeForm(forms.ModelForm):
    class Meta:
        model = CheckFileType
        fields = '__all__'



