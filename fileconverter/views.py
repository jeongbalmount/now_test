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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FileConvert(TemplateView):
    template_name = 'fileconverter/home.html'


def fileUpload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("after")
            url_list = form.clean_uploadedFiles()
            form_save = form.save()
            if len(url_list) == 1:
                fps_value_1 = form.cleaned_data['fps_value_1']
                scale_1 = form.cleaned_data['scaleValue_select_1']
                width_1, height_1 = define_scale(scale_1)
                first_url = form_save.first_uploaded_file
                # file_one_names = first_url.name
                s3_file_url = ('https://'
                               + settings.AWS_CLOUDFRONT_DOMAIN
                               + '/media/'
                               + first_url.name)
                gif_s3_url = make_gif(s3_file_url, fps_value_1, width_1, height_1)
                dict_urls = {'url_one': gif_s3_url}
                UploadModel.objects.all().delete()
            else:
                first_url = form_save.first_uploaded_file
                second_url = form_save.second_uploaded_file
                fps_value_1 = form.cleaned_data['fps_value_1']
                fps_value_2 = form.cleaned_data['fps_value_2']
                scale_1 = form.cleaned_data['scaleValue_select_1']
                scale_2 = form.cleaned_data['scaleValue_select_2']
                width_1, height_1 = define_scale(scale_1)
                width_2, height_2 = define_scale(scale_2)
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
                gif_s3_url_first = make_gif(s3_file_url_first, fps_value_1, width_1, height_1)
                gif_s3_url_second = make_gif(s3_file_url_second, fps_value_2, width_2, height_2)
                dict_urls = {'url_one': gif_s3_url_first, 'url_two': gif_s3_url_second}
                UploadModel.objects.all().delete()

            return JsonResponse(dict_urls, status=201)
        else:
            return JsonResponse(data=form.errors, status=400)


def URLupload(request):
    if request.method == 'POST':
        form = UploadURLForm(json.loads(request.body))
        if form.is_valid():
            print("after isvalid")
            valid_url = form.clean_uploadURL()
            url_scale = form.cleaned_data['URL_scaleValue_select']
            print(url_scale)
            url_fps = form.cleaned_data['URL_fps_value']
            print(url_fps)
            form.save()
            print("after save")
            urlInstance = UploadURLmodel(uploadURL=valid_url)
            file_url = urlInstance.save()
            # save()를 통해 나오는 것은 파일 이름!
            from_url_file_object_url = file_url
            file_name = basename(from_url_file_object_url)
            s3_file_url = ('https://'
                           + settings.AWS_CLOUDFRONT_DOMAIN
                           + '/media/'
                           + file_url)
            url_width, url_height = define_scale(url_scale)
            gif_s3_url = make_gif(s3_file_url, url_fps, url_width, url_height)
            dict_url = {'uploaded_file_url': gif_s3_url, 'file_name': file_name}
            UploadURLmodel.objects.all().delete()

            return JsonResponse(data=dict_url, status=201)
        else:
            errors = {'errors': 'errors'}
            return JsonResponse(data=errors, status=400)


def make_gif(s3_file_url, fps_value, input_width, input_height):
    # re_thing = re.compile('.+(?<=/)')
    _LENGTH = 12
    _LENGTH_2 = 15
    _MIDDLELEN = 3

    short_random_value = make_random_string(_MIDDLELEN)
    long_random_value = make_random_string(_LENGTH)

    random_rescale_filename = make_random_string(_LENGTH_2)
    random_palette_filename = str(round(random.random() * 100000000000))

    furl, file_extension = splitext(s3_file_url)

    out_file_name = "umzzalmaker-" + \
                    short_random_value + '-' + long_random_value + '.gif'
    out_rescale_or_not_file_name = "rescale-" + random_rescale_filename + '.{}'.format(file_extension)
    out_palette_name = "palette-"+random_palette_filename+'.png'
    limit_second_per_fps = 300  # fps25-> 12sec fps15 -> 20sec fps10 -> 30sec

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
        .filter('fps', fps=fps_value)
        .trim(start_frame=0, end_frame=limit_second_per_fps)
        .output('{}'.format(out_file_name))
        .run()
    )

    s3 = boto3.client('s3', config=Config(signature_version='s3v4'), aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    with open('{}'.format(out_file_name), "rb") as f:
        s3.upload_fileobj(f, "fileconvertstorage", "gif_file/{out_file_name}".format(out_file_name=out_file_name))

    os.remove('{}'.format(out_palette_name))
    os.remove('{}'.format(out_file_name))
    if input_width is not -1 or input_height is not -1:
        os.remove('{}'.format(out_rescale_or_not_file_name))

    bucket_name = "fileconvertstorage"
    object_name = "gif_file/{out_file_name}".format(out_file_name=out_file_name)
    presigned_url = create_presigned_url(s3, bucket_name, object_name)

    if presigned_url is None:
        return None

    print(presigned_url)
    # uploaded_file_url = ('https://'
    #     #                + settings.AWS_CLOUDFRONT_DOMAIN
    #     #                + '/gif_file/'
    #     #                + out_file_name)

    return presigned_url


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


def make_random_string(length):
    result = ""
    string_pool = string.ascii_letters + string.digits

    for i in range(length):
        result += random.choice(string_pool)

    return result


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




