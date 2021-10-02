from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = settings.AWS_S3_DOMAIN
        super(MediaStorage, self).__init__(*args, **kwargs)


