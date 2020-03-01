from django.contrib import admin
from django.urls import path, include
from .views import FileConvert

urlpatterns = [
    path('', FileConvert.as_view(), name='fileConvert' )
]
