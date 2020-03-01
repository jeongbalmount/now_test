from django.contrib import admin
from .models import UploadModel


@admin.register(UploadModel)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('uploadedFile', )
