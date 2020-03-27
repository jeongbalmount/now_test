import base64
import json
import ffmpeg
import re

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from .models import UploadModel, UploadURLmodel
from .forms import UploadFileForm, UploadURLForm, CheckTypeForm


class FileConvert(TemplateView):
    template_name = 'fileconverter/home.html'


@ensure_csrf_cookie
def fileUpload(request):
    dictNames = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fileList = request.FILES.getlist('uploadedFiles')
            keys = ['one', 'two']
            names = []
            if request.method == 'POST':
                for f in fileList:
                    names.append(f.name)
                dictNames = {keys[i]: names[i] for i in range(len(names))}
                print(dictNames)
            form.save()
            return JsonResponse(dictNames, status=201)
        else:
            return JsonResponse(data=form.errors, status=400)


def URLupload(request):
    if request.method == 'POST':
        form = UploadURLForm(json.loads(request.body))
        # valid_url = (json.loads(request.body))['uploadURL']
        if form.is_valid():
            valid_url = form.cleaned_data['uploadURL']
            urlInstance = UploadURLmodel(uploadURL=valid_url)
            wow = urlInstance.save()
            # fileName = urlInstance.save(valid_url)
            dictData = {'fileName': wow}
            return JsonResponse(data=dictData, status=201)
        else:
            errors = {'errors' : 'errors'}
            return JsonResponse(data=errors, status=400)


def convertFile(request):
    url_list = []
    if request.method == 'POST':
        form = CheckTypeForm(json.loads(request.body))
        if form.is_valid():
            form_type = form.cleaned_data['checkType']
            if form_type:
                files = UploadURLmodel.objects.all() # url이 넘어 온거면 파일 무조건 1개
                input_path_url = files.fileFromURL.path
                converted_url = convertByFF(input_path_url)
            else:
                files = UploadModel.objects.all()
                for item in files:
                    input_path = item.UploadedFiles.path
                    gif_file = convertByFF(input_path) # 일반 파일만 넘어 온거면 1개이상 2개 이하
                    url_list.append(gif_file)
        else:
            errors = {'errors': 'errors'}
            return JsonResponse(data=errors, status=400)


def convertByFF(input_url):
    re_thing = re.compile('.+(?<=/)')
    front_url = re_thing.findall(input_url)
    input_stream = ffmpeg.input('{}'.format(input_url))
    outFile = ffmpeg.output(input_stream, '')





# class FileUpload(BaseCreateView):
#     model = UploadModel
#     fields = ['uploadedFiles']
#
#     # 가져온 파일 모두 가져오기
#     # 비디오 파일 None아닌 상태 되도록 하기
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         print(self.request.POST)
#         fileList = self.request.FILES.getlist('uploadedFiles')
#         keys = ['one', 'two']
#         names = []
#         # dictNames = {}
#         if self.request.method == 'POST':
#             for f in fileList:
#                 names.append(f.name)
#             dictNames = {keys[i]: names[i] for i in range(len(names))}
#             kwargs['data'] = dictNames
#             print(kwargs['data'])
#             # print(kwargs['files'])
#         return kwargs
#
#     def form_valid(self, form):
#         print("form_valid()", form)
#         self.object = form.save()
#         names = (self.object).objects.values()
#
#         for f in names:
#             name = f.name
#             print(name)
#
#         files = model_to_dict(self.object)
#         print(f"files: {files}")
#         return JsonResponse(data=files, status=201)
#
#     def form_invalid(self, form):
#         return JsonResponse(data=form.errors, status=400)
#
#
# # class Temporary(TemplateView):
#     template_name = 'fileconverter/temp.html'