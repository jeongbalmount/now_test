from django.contrib import admin
from .models import UploadModel, UploadURLmodel


@admin.register(UploadModel)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('uploadedFiles',)


@admin.register(UploadURLmodel)
class UploadURLAdmin(admin.ModelAdmin):
    list_display = ('uploadURL', 'fileFromURL')