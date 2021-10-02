import math
import ffmpeg
import re
from os import path
from django.core.validators import URLValidator
from django import forms

from .models import UploadModel, UploadURLmodel


# 비디오 파일 넘어 왔을때 유효성 검사
class UploadFileForm(forms.ModelForm):
    max_size = 52428800
    videoTypes = ['video/avi', 'video/webm', 'video/quicktime'
                  ,'video/x-matroska', 'video/x-ms-wmv', 'video/mpeg', 'video/x-flv', 'video/mp4']
    scaleTypes = ["변환할 동영상 해상도(기본)", "가로:600px", "가로:480px", "세로:480px", "세로:320px"]

    class Meta:
        model = UploadModel
        fields = ['first_uploaded_file', 'second_uploaded_file', 'fps_value_1', 'fps_value_2',
                  'scaleValue_select_1', 'scaleValue_select_2', 'start_1', 'start_2', 'end_1', 'end_2',
                  'use_palette_1', 'use_palette_2']

    def clean_uploadedFiles(self):
        print("clean_uploadedFiles")
        # cleaned_data
        first_file = self.cleaned_data['first_uploaded_file']
        second_file = self.cleaned_data['second_uploaded_file']
        scale_1 = self.cleaned_data['scaleValue_select_1']
        scale_2 = self.cleaned_data['scaleValue_select_2']
        fps_value_1 = self.cleaned_data['fps_value_1']
        fps_value_2 = self.cleaned_data['fps_value_2']
        start_1 = self.cleaned_data['start_1']
        start_2 = self.cleaned_data['start_2']
        end_1 = self.cleaned_data['end_1']
        end_2 = self.cleaned_data['end_2']
        use_palette_1 = self.cleaned_data['use_palette_1']
        use_palette_2 = self.cleaned_data['use_palette_2']
        file_url_list = []
        valid_file_boolean = True

        # 한개의 파일만 들어 올때
        if first_file is not None and second_file is None:
            print("No second file")
            check_first_file = first_file.content_type
            all_file_size = first_file.size

            # 시작시간, 끝나는 시간 유효성 검사
            error_message, valid_file_boolean = valid_one_file(start_1, end_1)
            if valid_file_boolean is False:
                return error_message, valid_file_boolean

            if check_first_file not in self.videoTypes:
                error_message = "mp4와 같은 비디오 파일을 입력해 주세요"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if scale_1 not in self.scaleTypes:
                error_message = "맞는 해상도가 아닙니다"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            # 50MB를 넘었을때
            if all_file_size > self.max_size:
                error_message = "파일 전체 크기가 너무 큽니다."
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if fps_value_1 > 25:
                error_message = "fps크기 초과"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_1 is not 1 and use_palette_1 is not 0:
                error_message = "고화질 저화질 옵션 오류"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            file_url_list.append(first_file)

        elif first_file is not None and second_file is not None:
            print("two files")
            check_first_file = first_file.content_type
            check_second_file = second_file.content_type
            all_file_size = first_file.size + second_file.size

            error_message, valid_file_boolean = valid_two_files(start_1, start_2, end_1, end_2)

            # 비디오 파일이 아닐시
            if check_first_file not in self.videoTypes or check_second_file not in self.videoTypes:
                error_message = "mp4와 같은 비디오 파일을 입력해 주세요"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if scale_1 not in self.scaleTypes or scale_2 not in self.scaleTypes:
                error_message = "맞는 해상도가 아닙니다"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if all_file_size > self.max_size:
                error_message = "파일 전체 크기가 너무 큽니다"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if fps_value_1 > 25 or fps_value_2 > 25:
                error_message = "fps크기 초과"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_1 is not 1 and use_palette_1 is not 0:
                error_message = "고화질 저화질 옵션 오류"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_2 is not 1 and use_palette_2 is not 0:
                error_message = "고화질 저화질 옵션 오류"
                valid_file_boolean = False
                return error_message, valid_file_boolean
            file_url_list.append(first_file)
            file_url_list.append(second_file)
        print("before return")
        return file_url_list, valid_file_boolean


# URL로 받았을때
class UploadURLForm(forms.ModelForm):
    videoTypes = ['avi', 'flv', 'wmv', 'mov', 'mp4', 'webm', 'mkv', 'mpeg']
    scaleTypes = ["변환할 동영상 해상도(기본)", "가로:600px", "가로:480px", "세로:480px", "세로:320px"]
    max_size = 52428800

    class Meta:
        model = UploadURLmodel
        fields = ['use_palette_2', 'use_palette_1', 'URL_end_2', 'URL_end_1', 'URL_start_2', 'URL_start_1',
                  'URL_scaleValue_select_2', 'URL_scaleValue_select_1',
                  'URL_fps_value_2', 'URL_fps_value_1', 'uploadURL_2', 'uploadURL_1']

    def clean_uploadURLs(self):
        print("this is form inside forms")
        uploadURL = self.cleaned_data['uploadURL_1']
        uploadURL_2 = self.cleaned_data['uploadURL_2']
        file_scale_value = self.cleaned_data['URL_scaleValue_select_1']
        file_scale_value_2 = self.cleaned_data['URL_scaleValue_select_2']
        file_fps = self.cleaned_data['URL_fps_value_1']
        file_fps_2 = self.cleaned_data['URL_fps_value_2']
        file_start = self.cleaned_data['URL_start_1']
        file_start_2 = self.cleaned_data['URL_start_2']
        file_end = self.cleaned_data['URL_end_1']
        file_end_2 = self.cleaned_data['URL_end_2']
        use_palette_1 = self.cleaned_data['use_palette_1']
        use_palette_2 = self.cleaned_data['use_palette_2']
        # 파일 url 받아서 파싱한 후 저장
        url_list = []
        valid_file_boolean = True
        file_url = uploadURL
        file_url_2 = uploadURL_2
        furl, file_extension = path.splitext(file_url)

        # 시작시간, 끝나는 시간 유효성 검사
        if uploadURL is not None and uploadURL_2 is None:
            error_message, valid_file_boolean = valid_one_file(file_start, file_end)
            if valid_file_boolean is False:
                return error_message, valid_file_boolean

            if URLValidator(file_url) is False:
                error_message = "Please write down the exact url format"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if file_fps > 25:
                error_message = "fps max size exceeded"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if file_scale_value not in self.scaleTypes:
                error_message = "resolution error"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            try:
                url_file_size = ffmpeg.probe(uploadURL)['format']['size']
                url_is_video_format = ffmpeg.probe(uploadURL)['format']['format_long_name']
                url_file_size = int(url_file_size)
            except:
                error_message = "It's not a video file"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            comp = re.compile('\w+$')
            m = comp.findall(url_is_video_format)
            lower_video_type = m[0].lower()

            if lower_video_type not in self.videoTypes:
                error_message = "Not a supported video format"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if url_file_size > self.max_size:
                error_message = "Video file size exceeded 50M"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_1 is not 1 and use_palette_1 is not 0:
                error_message = "High Definition Low Definition Option Error"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            url_list.append(file_url)

        elif uploadURL is not None and uploadURL_2 is not None:
            # furl_2, file_extension_2 = path.splitext(file_url_2)
            error_message, valid_file_boolean = valid_two_files(file_start, file_start_2, file_end, file_end_2)
            if valid_file_boolean is False:
                return error_message, valid_file_boolean

            if URLValidator(file_url) is False or URLValidator(file_url_2) is False:
                error_message = "Please write down the exact url format"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if file_fps > 25 or file_fps_2 > 25:
                error_message = "fps max size exceeded"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if file_scale_value not in self.scaleTypes or file_scale_value_2 not in self.scaleTypes:
                error_message = "resolution error"
                valid_file_boolean = False
                return error_message, valid_file_boolean
            try:
                url_file_size = ffmpeg.probe(uploadURL)['format']['size']
                url_file_size = int(url_file_size)
                url_file_size_2 = ffmpeg.probe(uploadURL_2)['format']['size']
                url_file_size_2 = int(url_file_size_2)
                total_size = url_file_size + url_file_size_2
                url_is_video_format_1 = ffmpeg.probe(uploadURL)['format']['format_long_name']
                url_is_video_format_2 = ffmpeg.probe(uploadURL_2)['format']['format_long_name']
            except:
                error_message = "It's not a video file"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            comp = re.compile('\w+$')
            m = comp.findall(url_is_video_format_1)
            lower_video_type_1 = m[0].lower()

            m2 = comp.findall(url_is_video_format_2)
            lower_video_type_2 = m2[0].lower()

            if lower_video_type_1 not in self.videoTypes or lower_video_type_2 not in self.videoTypes:
                error_message = "Not a supported video format"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if total_size > self.max_size:
                error_message = "Total video file size exceeded 50M"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_1 is not 1 and use_palette_1 is not 0:
                error_message = "High Definition Low Definition Option Error"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            if use_palette_2 is not 1 and use_palette_2 is not 0:
                error_message = "High Definition Low Definition Option Error"
                valid_file_boolean = False
                return error_message, valid_file_boolean

            url_list.append(file_url)
            url_list.append(file_url_2)

        return url_list, valid_file_boolean


def isfloat_and_int(input_value):
    if type(input_value) is float or type(input_value) is int:
        return True
    else:
        return False


def valid_one_file(input_start, input_end):
    error_message = "no error"
    valid_file_boolean = True
    input_end_isdefault = math.isclose(input_end, -1.0) # 끝나는 값이 동영상 끝나는 값일때

    if input_end_isdefault is False:
        if input_start > input_end:
            error_message = "End time must be greater than start time"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_end == 0:
            error_message = "The ending time is zero"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_start < 0 or input_end < 0:
            error_message = "Time must be greater than zero"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if isfloat_and_int(input_start) is False or isfloat_and_int(input_end) is False:
            error_message = "Please write down the number up to the second decimal point"
            valid_file_boolean = False
            return error_message, valid_file_boolean

    elif input_end_isdefault is True:
        if input_start < 0:
            error_message = "Please write down the number up to the second decimal point"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if isfloat_and_int(input_start) is False:
            error_message = "Please write down the number up to the second decimal point"
            valid_file_boolean = False
            return error_message, valid_file_boolean

    return error_message, valid_file_boolean


# 비디오 파일이 2개 들어왔을때 2개에 대한 시작시간 끝나는 시간 유효성 검사
def valid_two_files(input_start_1, input_start_2, input_end_1, input_end_2):
    input_end_1_isdefault = math.isclose(input_end_1, -1.0)
    input_end_2_isdefault = math.isclose(input_end_2, -1.0)

    error_message = "no error"
    valid_file_boolean = True
    if input_end_1_isdefault is False and input_end_2_isdefault is False:
        if isfloat_and_int(input_start_1) is False or isfloat_and_int(input_end_1) is False:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if isfloat_and_int(input_start_2) is False or isfloat_and_int(input_end_2) is False:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_start_1 > input_end_1:
            error_message = "Start time is greater than end time. Please correct it."
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if input_start_2 > input_end_2:
            error_message = "Start time is greater than end time. Please correct it."
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_end_1 is 0 or input_end_2 is 0:
            error_message = "Please correct the ending time"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_start_1 < 0 or input_start_2 < 0:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean

        if input_end_1 < 0 or input_end_2 < 0:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean

    elif input_end_1_isdefault is True and input_end_2_isdefault is False:
        if isfloat_and_int(input_start_1) is False or isfloat_and_int(input_end_2) \
                is False or isfloat_and_int(input_start_2) is False:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if isfloat_and_int(input_start_1) < 0 or isfloat_and_int(input_end_2) < 0 or isfloat_and_int(input_start_2) < 0:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if input_start_2 > input_end_2:
            error_message = "Start time is greater than end time. Please correct it."
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if input_end_2 == 0:
            error_message = "Please correct the ending time"
            valid_file_boolean = False
            return error_message, valid_file_boolean

    elif input_end_1_isdefault is False and input_end_2_isdefault is True:
        if isfloat_and_int(input_start_1) is False or isfloat_and_int(input_end_1) is False \
                or isfloat_and_int(input_start_2) is False:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if isfloat_and_int(input_start_1) < 0 or isfloat_and_int(input_end_1) < 0 or isfloat_and_int(
            input_start_2) < 0:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if input_start_1 > input_end_1:
            error_message = "Start time is greater than end time. Please correct it."
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if input_end_1 == 0:
            error_message = "Please correct the ending time"
            valid_file_boolean = False
            return error_message, valid_file_boolean
    elif input_end_1_isdefault is True and input_end_2_isdefault is True:
        if isfloat_and_int(input_start_1) is False or isfloat_and_int(input_start_2) is False:
            error_message = "Please enter a number greater than 0 (set to 2 decimal places)"
            valid_file_boolean = False
            return error_message, valid_file_boolean
        if isfloat_and_int(input_start_1) < 0 or isfloat_and_int(input_start_2) < 0:
            error_message = "Please correct the start time"
            valid_file_boolean = False
            return error_message, valid_file_boolean

    return error_message, valid_file_boolean

