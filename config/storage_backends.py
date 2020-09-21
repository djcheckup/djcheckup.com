from storages.backends.s3boto3 import S3Boto3Storage
from .settings import AWS_LOCATION


class StaticStorage(S3Boto3Storage):
    location = AWS_LOCATION
    default_acl = "public-read"
