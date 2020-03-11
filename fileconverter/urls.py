from django.contrib import admin
from django.urls import path, include
from .views import FileConvert, FileUpload

app_name = "fileconverter"
urlpatterns = [
    path('', FileConvert.as_view(), name='fileConvert'),
    path('convert/upload/', FileUpload, name='upload'),
    # path('success/url', Temporary.as_view(), name='temp'),
]
