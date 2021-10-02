from django.contrib import admin
from .models import UploadModel, UploadURLmodel

@admin.register(UploadModel)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('first_uploaded_file', 'second_uploaded_file')


@admin.register(UploadURLmodel)
class UploadURLAdmin(admin.ModelAdmin):
    list_display = ['uploadURL_1']

