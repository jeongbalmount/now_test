from os import path
from django.core.validators import URLValidator
from django import forms

from .models import UploadModel, UploadURLmodel


class UploadFileForm(forms.ModelForm):
    max_size = 52428800
    videoTypes = ['video/avi', 'video/webm', 'video/quicktime'
                  ,'video/x-matroska', 'video/x-ms-wmv', 'video/mpeg', 'video/x-flv', 'video/mp4']
    scaleTypes = ["변환할 동영상 해상도(기본)", "가로:600px", "가로:480px", "세로:480px", "세로:320px"]

    class Meta:
        model = UploadModel
        fields = ['first_uploaded_file', 'second_uploaded_file', 'fps_value_1', 'fps_value_2',
                  'scaleValue_select_1', 'scaleValue_select_2']

    def clean_uploadedFiles(self):
        print("clean_uploadedFiles")
        first_file = self.cleaned_data['first_uploaded_file']
        second_file = self.cleaned_data['second_uploaded_file']
        scale_1 = self.cleaned_data['scaleValue_select_1']
        scale_2 = self.cleaned_data['scaleValue_select_2']
        fps_value_1 = self.cleaned_data['fps_value_1']
        fps_value_2 = self.cleaned_data['fps_value_2']
        print(fps_value_1)
        file_url_list = []

        if first_file is not None and second_file is None:
            print("No second file")
            check_first_file = first_file.content_type
            all_file_size = first_file.size
            if check_first_file not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')
                # 50MB를 넘었을때
            if scale_1 not in self.scaleTypes:
                print('해상도 오류')
                raise forms.ValidationError('맞는 해상도가 아닙니다')

            if all_file_size > self.max_size:
                print('파일 크기')
                raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

            if fps_value_1 > 25:
                print('fps 최대 크기 초과')
                raise forms.ValidationError('fps크기 초과')
            file_url_list.append(first_file)

        elif first_file is not None and second_file is not None:
            check_first_file = first_file.content_type
            check_second_file = second_file.content_type
            print(check_first_file)
            print(check_second_file)
            all_file_size = first_file.size + second_file.size
            # 비디오 파일이 아닐시
            if check_first_file not in self.videoTypes or check_second_file not in self.videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')

            if scale_1 not in self.scaleTypes or scale_2 not in self.scaleTypes:
                print('해상도 오류')
                raise forms.ValidationError('맞는 해상도가 아닙니다')

            if all_file_size > self.max_size:
                print('파일 크기')
                raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

            if fps_value_1 > 25 or fps_value_2 > 25:
                print('fps 최대 크기 초과')
                raise forms.ValidationError('fps크기 초과')
            file_url_list.append(first_file)
            file_url_list.append(second_file)

        return file_url_list


class UploadURLForm(forms.ModelForm):
    videoTypes = ['avi', 'flv', 'wmv', 'mov', 'mp4', 'webm', 'mkv', 'mpeg']
    scaleTypes = ["변환할 동영상 해상도(기본)", "가로:600px", "가로:480px", "세로:480px", "세로:320px"]

    class Meta:
        model = UploadURLmodel
        fields = ['URL_scaleValue_select', 'URL_fps_value', 'uploadURL', 'URL_start', 'URL_end']

    def clean_uploadURL(self):
        print("this is form")
        uploadURL = self.cleaned_data['uploadURL']
        print(uploadURL)
        file_scale_value = self.cleaned_data['URL_scaleValue_select']
        print(file_scale_value)
        file_fps = self.cleaned_data['URL_fps_value']
        print(file_fps)
        # 파일 url 받아서 파싱한 후 저장
        file_url = uploadURL
        furl, file_extension = path.splitext(file_url)
        if URLValidator(file_url) is False and file_extension not in self.videoTypes:
            print("raised")
            raise forms.ValidationError('정확한 url형식을 적어주세요')

        if file_fps > 25:
            print('fps 최대 크기 초과')
            raise forms.ValidationError('fps크기 초과')

        if file_scale_value not in self.scaleTypes:
            print('해상도 오류')
            raise forms.ValidationError('맞는 해상도가 아닙니다')

        print("before return")
        return uploadURL






