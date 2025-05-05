from minio import Minio
from core.config import settings

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=True,
)

if not client.bucket_exists(settings.MINIO_BUCKET):
    client.make_bucket(settings.MINIO_BUCKET)