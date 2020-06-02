import json
import ffmpeg
import random
import string
import boto3
import os
import logging

from os.path import basename, splitext

from botocore.config import Config
from django.utils.decorators import method_decorator

from config import settings

from botocore.exceptions import ClientError

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from .models import UploadURLmodel, UploadModel
from .forms import UploadFileForm, UploadURLForm


# csrf 쿠키를 위한 데코레이터
@method_decorator(ensure_csrf_cookie, name='dispatch')
class FileConvert(TemplateView):
    template_name = 'fileconverter/home.html'
    # 처음 홈페이지 제공


# url이 아닌 파일 업로드시 사용하는 함수
def fileUpload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 폼데이터를 받는 부분
        if form.is_valid():
            # 오류 메시지나 파일 url을 받고 2번째는 오류냐 아니냐를 판단
            url_list_or_message, valid_file_boolean = form.clean_uploadedFiles()
            # 오류면 메시지 리턴
            if valid_file_boolean is False:
                errors = {'errors': url_list_or_message}
                return JsonResponse(data=errors, status=400)
            # form데이터를 db에 저장
            form_save = form.save()
            # 비디오 파일이 1개 들어왔을때
            if len(url_list_or_message) == 1:
                fps_value_1 = form.cleaned_data['fps_value_1']
                scale_1 = form.cleaned_data['scaleValue_select_1']
                start_1 = form.cleaned_data['start_1']
                end_1 = form.cleaned_data['end_1']
                # 리스케일값 유효성 검사
                width_1, height_1 = define_scale(scale_1)
                # 저장한 폼데이터 값 중 비디오 url가져오기
                first_url = form_save.first_uploaded_file
                # file_one_names = first_url.name
                # s3에 저장된 비디오 url을 불러오기
                s3_file_url = ('https://'
                               + settings.AWS_CLOUDFRONT_DOMAIN
                               + '/media/'
                               + first_url.name)
                # 시작 시간, 끝나는 시간 유효성 검사
                start_end_valid, message_or_end = validate_start_end_time(s3_file_url, start_1, end_1)
                # 틀리면 오류 메시지 리턴
                if start_end_valid is False:
                    errors = {'errors': message_or_end}
                    return JsonResponse(data=errors, status=400)
                # 파일 gif로 바꾸기
                gif_s3_url = make_gif(s3_file_url, fps_value_1, width_1, height_1, start_1, message_or_end)
                dict_urls = {'url_one': gif_s3_url}
                # 로컬에 남아 있는 모델 데이터 지우기
                UploadModel.objects.all().delete()
            else:   # 비디오 파일이 2개 넘어 올때
                first_url = form_save.first_uploaded_file
                second_url = form_save.second_uploaded_file
                fps_value_1 = form.cleaned_data['fps_value_1']
                fps_value_2 = form.cleaned_data['fps_value_2']
                scale_1 = form.cleaned_data['scaleValue_select_1']
                scale_2 = form.cleaned_data['scaleValue_select_2']
                width_1, height_1 = define_scale(scale_1)
                width_2, height_2 = define_scale(scale_2)
                start_1 = form.cleaned_data['start_1']
                end_1 = form.cleaned_data['end_1']
                start_2 = form.cleaned_data['start_2']
                end_2 = form.cleaned_data['end_2']
                # file_one_name = first_url.name
                # file_two_name = second_url.name
                s3_file_url_first = ('https://'
                                     + settings.AWS_CLOUDFRONT_DOMAIN
                                     + '/media/'
                                     + first_url.name)
                s3_file_url_second = ('https://'
                                      + settings.AWS_CLOUDFRONT_DOMAIN
                                      + '/media/'
                                      + second_url.name)
                start_end_valid_1, message_or_end_1 = validate_start_end_time(s3_file_url_first, start_1, end_1)
                start_end_valid_2, message_or_end_2 = validate_start_end_time(s3_file_url_second, start_2, end_2)
                if start_end_valid_1 is False or start_end_valid_2 is False:
                    errors = {'errors': '동영상 전체 길이를 초과 하였습니다'}
                    return JsonResponse(data=errors, status=400)

                gif_s3_url_first = make_gif(s3_file_url_first, fps_value_1, width_1, height_1, start_1,
                                            message_or_end_1)
                gif_s3_url_second = make_gif(s3_file_url_second, fps_value_2, width_2, height_2, start_2,
                                             message_or_end_2)
                dict_urls = {'url_one': gif_s3_url_first, 'url_two': gif_s3_url_second}
                UploadModel.objects.all().delete()

            return JsonResponse(dict_urls, status=201)
        else:
            return JsonResponse(data=form.errors, status=400)


# 비디오 파일 url이 넘어 올때
def URLupload(request):
    if request.method == 'POST':
        # 비디오파일 url과 설정 데이터가 넘어올때
        form = UploadURLForm(json.loads(request.body))
        form_valid = form.is_valid()
        if form_valid:
            # valid_url = form.clean_uploadURL()
            url_scale = form.cleaned_data['URL_scaleValue_select']
            url_fps = form.cleaned_data['URL_fps_value']
            url_start = form.cleaned_data['URL_start']
            url_end = form.cleaned_data['URL_end']
            file_url = form.save()
            # save()를 통해 나오는 것은 파일 이름!
            # file_url이 model타입이기 때문에 str형식인 name사용
            from_url_file_object_url = file_url.fileFromURL.name
            file_name = basename(from_url_file_object_url)
            s3_file_url = ('https://'
                           + settings.AWS_CLOUDFRONT_DOMAIN
                           + '/media/'
                           + from_url_file_object_url)
            url_width, url_height = define_scale(url_scale)
            start_end_valid, URL_message_or_end = validate_start_end_time(s3_file_url, url_start, url_end)
            if start_end_valid is False:
                errors = {'errors': URL_message_or_end}
                return JsonResponse(data=errors, status=400)
            gif_s3_url = make_gif(s3_file_url, url_fps, url_width, url_height, url_start, URL_message_or_end)
            dict_url = {'uploaded_file_url': gif_s3_url, 'file_name': file_name}
            UploadURLmodel.objects.all().delete()

            return JsonResponse(data=dict_url, status=201)
        else:
            errors = {'errors': 'errors'}
            return JsonResponse(data=errors, status=400)


def make_gif(s3_file_url, fps_value, input_width, input_height, input_start, input_end):
    # re_thing = re.compile('.+(?<=/)')
    # 파일 이름을 구성하는 난수를 위한 const변수들
    _LENGTH = 12
    _LENGTH_2 = 15
    _MIDDLELEN = 3

    # 파일 이름 구성하는 변수들
    short_random_value = make_random_string(_MIDDLELEN)
    long_random_value = make_random_string(_LENGTH)

    # 리스케일링 된 파일의 이름, 팔레트 png 파일이름
    random_rescale_filename = make_random_string(_LENGTH_2)
    random_palette_filename = str(round(random.random() * 100000000000))

    # 비디오 파일 리스케일시 파일 확장자에 붙여줄 확장자 뽑는 과정
    furl, file_extension = splitext(s3_file_url)

    # 변환 파일이름 구하는 변수
    out_file_name = "umzzalmaker-" + \
                    short_random_value + '-' + long_random_value + '.gif'
    # 리스케일된 비디오 파일 이름 변수
    out_rescale_or_not_file_name = "rescale-" + random_rescale_filename + '.{}'.format(file_extension)
    # 팔레트 이름 변수
    out_palette_name = "palette-"+random_palette_filename+'.png'
    # limit_second_per_fps = 300  # fps25-> 12sec fps15 -> 20sec fps10 -> 30sec

    # 각 fps에 맞는 제한 시간에 전체 재생시간을 맞춘다
    valid_end = limit_time_by_frame(fps_value, input_start, input_end)

    # 기본 해상도로 설정되어 있지 않으면 리스케일한다.
    if input_width is not -1 or input_height is not -1:
        (
            ffmpeg
            .input(s3_file_url)
            .filter('scale', input_width, input_height)
            .output('{}'.format(out_rescale_or_not_file_name), format='mp4')
            .run(overwrite_output=True)
        )
    else:
        out_rescale_or_not_file_name = s3_file_url

    # 움짤의 선명도를 높이기 위해 palette생성
    (
        ffmpeg
        .input(out_rescale_or_not_file_name)
        .filter(filter_name='palettegen', stats_mode='full')
        .output('{}'.format(out_palette_name))
        .run()
    )
    # 비디오 파일을 움짤로 바꿀때 팔레트와 함성하는 작업
    (
        ffmpeg.filter(
            [
                ffmpeg.input(out_rescale_or_not_file_name),
                ffmpeg.input('{}'.format(out_palette_name))
            ],
            filter_name='paletteuse',
            dither='heckbert',
            new='False',
        )
        .filter('fps', fps=fps_value)# fps적용하기
        .trim(start=input_start, end=valid_end) # 시작시간, 끝나는 시간 정해주
        .output('{}'.format(out_file_name))
        .run()
    )

    # s3 사용가능하게 만들기
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'), aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    # s3에 업로드 하기
    with open('{}'.format(out_file_name), "rb") as f:
        s3.upload_fileobj(f, "fileconvertstorage", "gif_file/{out_file_name}".format(out_file_name=out_file_name))
    # 로컬에 남아 있는 파일들 지우기
    os.remove('{}'.format(out_palette_name))
    os.remove('{}'.format(out_file_name))
    # 너비나 높이 중 하나라도 수정되었다면 리스케일링 된 비디오 파일 지우기
    if input_width is not -1 or input_height is not -1:
        os.remove('{}'.format(out_rescale_or_not_file_name))

    bucket_name = "fileconvertstorage"
    object_name = "gif_file/{out_file_name}".format(out_file_name=out_file_name)
    # presigned_url 만들기
    presigned_url = create_presigned_url(s3, bucket_name, object_name)

    if presigned_url is None:
        return None

    print(presigned_url)
    # uploaded_file_url = ('https://'
    #     #                + settings.AWS_CLOUDFRONT_DOMAIN
    #     #                + '/gif_file/'
    #     #                + out_file_name)

    return presigned_url


# 시간이 지나면 사라지는 url을 만드는 함수
def create_presigned_url(s3, bucket_name, object_name, expiration=3600):
    try:
        response = s3.generate_presigned_url(ClientMethod='get_object',
                                         Params={'Bucket': bucket_name,
                                                 'Key': object_name},
                                         ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response


# 랜덤한 숫자+문자를 만들어낸다.
def make_random_string(length):
    result = ""
    string_pool = string.ascii_letters + string.digits

    for i in range(length):
        result += random.choice(string_pool)

    return result


# 해상도를 결정하는 함수
def define_scale(input_scale):
    width = -1
    height = -1

    if input_scale == "가로:600px":
        width = 600
        height = -2
    elif input_scale == "가로:480px":
        width = 480
        height = -2
    elif input_scale == "세로:480px":
        width = -2
        height = 480
    elif input_scale == "세로:320px":
        width = -2
        height = 320

    return width, height


# 전체 동영상 길이를 넘지만 않으면 된다. 프레임으로 제한 주는 것은 밑 함수가 담당한다.
def validate_start_end_time(input_file_url, input_start, input_end):
    file_url = input_file_url
    duration = ffmpeg.probe(file_url)['format']['duration']
    duration = float(duration)

    if input_start > duration or input_end > duration:
        error_message = '동영상 전체 길이를 초과 하였습니다'
        return False, error_message

    elif input_end is -1:
        return True, duration

    else:
        return True, input_end


# 프레임 별로 limit초를 나누어 제한한다.
def limit_time_by_frame(fps_value, input_start, input_end):

    time_value = input_end - input_start
    if fps_value is 25:
        if time_value > 12:
            input_end = input_start + 12
            return input_end
        else:
            return input_end
    elif fps_value is 15:
        if time_value > 20:
            input_end = input_start + 20
            return input_end
        else:
            return input_end
    else:
        if time_value > 30:
            input_end = input_start + 30
            return input_end
        else:
            return input_end





