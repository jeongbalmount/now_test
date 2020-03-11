from django import forms
from .models import UploadModel
import filetype


class UploadFileForm(forms.ModelForm):
    max_size = 10485760

    class Meta:
        model = UploadModel
        fields = ['uploadedFiles',]

    def clean_uploadedFiles(self):
        uploadFiles = self.cleaned_data['uploadedFiles']
        uploadFileList = self.files.getlist('uploadedFiles')
        videoTypes = ['video/x-m4v', 'video/x-matroska', 'video/webm', 'video/quicktime',
                      'video/x-msvideo', 'video/x-ms-wmv', 'video/mpeg', 'video/x-flv', 'video/mp4']
        AllfileSize = 0

        for filesize in uploadFileList:
            AllfileSize = filesize.size
            print(filesize.size)
        # 50MB를 넘었을때
        if AllfileSize > self.max_size:
            print('파일 크기')
            raise forms.ValidationError('파일 전체 크기가 너무 큽니다.')

        for file in uploadFileList:
            # print(file)
            checkfile = filetype.guess(file)
            print(checkfile.mime)

            # 비디오 파일이 아닐시
            if checkfile.mime not in videoTypes:
                print('파일 형식')
                raise forms.ValidationError('mp4와 같은 비디오 파일을 입력해 주세요')


            print('File extension: %s' % checkfile.extension)
            print('File MIME type: %s' % checkfile.mime)
        print(uploadFileList)

        return uploadFiles