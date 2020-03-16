from django.contrib import admin
from django.urls import path, include
from .views import FileConvert, FileUpload, URLupload

app_name = "fileconverter"
urlpatterns = [
    path('', FileConvert.as_view(), name='fileConvert'),
    path('convert/upload/', FileUpload, name='upload'),
    path('convert/urlupload/', URLupload, name='URLupload'),
    # path('success/url', Temporary.as_view(), name='temp'),
]
