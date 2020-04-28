from os import path
from django.core.validators import URLValidator
from django import forms

from .models import UploadModel, UploadURLmodel


class UploadFileForm(forms.ModelForm):
    max_size = 52428800
    videoTypes = ['video/x-m4v', 'video/x-matroska', 'video/webm', 'video/quicktime',
                  'video/x-msvideo', 'video/x-ms-wmv', 'video/mpeg', 'video/x-flv', 'video/mp4']

    class Meta:
        model = UploadModel
        fields = ['first_uploaded_file', 'second_uploaded_file', 'fps_value_1', 'fps_value_2']

    def clean_uploadedFiles(self):
        print("clean_uploadedFiles")
        first_file = self.cleaned_data['first_uploaded_file']
        second_file = self.cleaned_data['second_uploaded_file']
        fps_value_1 = self.cleaned_data['fps_value_1']
        fps_value_2 = self.cleaned_data['fps_value_2']
        file_url_list = []

        if second_file is None:
            print("No second file")
            check_first_file = first_file.content_type
            AllfileSize = first_file.size
            if check_first_file not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')
                # 50MB를 넘었을때
            file_url_list.append(first_file)

        else:
            check_first_file = first_file.content_type
            check_second_file = second_file.content_type
            AllfileSize = first_file.size + second_file.size
            # 비디오 파일이 아닐시
            if check_first_file and check_second_file not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')
            file_url_list.append(first_file)
            file_url_list.append(second_file)

        if AllfileSize > self.max_size:
            print('파일 크기')
            raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

        if fps_value_1 > 25 or fps_value_2 > 25:
            print('fps 최대 크기 초과')
            raise forms.ValidationError('fps크기 초과')

        return file_url_list


class UploadURLForm(forms.ModelForm):
    class Meta:
        model = UploadURLmodel
        fields = ['uploadURL', 'fileFromURL']
        videoTypes = ['avi', 'flv', 'wmv', 'mov', 'mp4', 'webm']

    def clean_uploadURL(self):
        print("this is form")
        uploadURL = self.cleaned_data['uploadURL']
        # 파일 url 받아서 파싱한 후 저장
        file_url = uploadURL
        furl, file_extension = path.splitext(file_url)
        if URLValidator(file_url) is False and file_extension not in self.videoTypes:
            print("raised")
            raise forms.ValidationError('정확한 url형식을 적어주세요')

        print("before return")
        return uploadURL






