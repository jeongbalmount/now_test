from django.contrib import admin
from django.urls import path, include
from .views import FileConvert, fileUpload, URLupload

app_name = "fileconverter"
urlpatterns = [
    path('', FileConvert.as_view(), name='fileConvert'),
    path('convert/upload/', fileUpload, name='upload'),
    path('convert/urlupload/', URLupload, name='URLupload'),
]
