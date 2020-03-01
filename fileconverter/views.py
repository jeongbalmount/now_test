from django.shortcuts import render
from django.views.generic import TemplateView


class FileConvert(TemplateView):
    template_name = 'fileconverter/home.html'
