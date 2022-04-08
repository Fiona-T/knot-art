"""To specify where static files and uploaded media files are to be stored"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    class inheriting from S3Boto3Storage
    Store static files in the location set in settings.py
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    class inheriting from S3Boto3Storage
    Store media files in the location set in settings.py
    """
    location = settings.MEDIAFILES_LOCATION
