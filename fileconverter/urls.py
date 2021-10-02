from django.contrib import admin
from django.urls import path
from .views import fileUpload, URLupload, FileConvert
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


app_name = "fileconverter"

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('', FileConvert.as_view(), name='index'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt",
         content_type='text/plain')),
    path('sitemap.xml/', TemplateView.as_view(template_name="sitemap.xml",
         content_type='text/xml')),
    path('convert/upload/', fileUpload, name='upload'),
    path('convert/urlupload/', URLupload, name='URLupload'),
]
