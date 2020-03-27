from django.contrib import admin
from .models import UploadModel, UploadURLmodel, CheckFileType


@admin.register(UploadModel)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('uploadedFiles',)


@admin.register(UploadURLmodel)
class UploadURLAdmin(admin.ModelAdmin):
    list_display = ('uploadURL', 'fileFromURL')


@admin.register(CheckFileType)
class UploadURLAdmin(admin.ModelAdmin):
    list_display = ('checkType',)