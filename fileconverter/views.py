import base64
import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.views.generic.edit import BaseCreateView

from .models import UploadModel
from .forms import UploadFileForm


class FileConvert(TemplateView):
    template_name = 'fileconverter/home.html'


@ensure_csrf_cookie
def FileUpload(request):
    data = None
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