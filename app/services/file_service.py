import io
import uuid
from fastapi import UploadFile
from core.minio_client import client
from core.config import settings
from repositories.file_repository import FileRepository
from schemas.file_schemas import FileMetaCreate

class FileService:
    def __init__(self, repo: FileRepository, db_session):
        self.repo = repo
        self.db = db_session

    async def upload(self, file: UploadFile):
        # Generate UUID
        file_id = str(uuid.uuid4())
        ext = file.filename.split('.')[-1]
        object_name = f"{file_id}.{ext}"
        data = await file.read()
        size = len(data)

        # Upload to MinIO
        client.put_object(
            settings.MINIO_BUCKET,
            object_name,
            io.BytesIO(data),
            size,
            content_type=file.content_type
        )
        url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_name}"

        # Save metadata
        meta = FileMetaCreate(
            id=file_id,
            filename=file.filename,
            content_type=file.content_type,
            url=url,
            size=size
        )
        return self.repo.save_metadata(meta)

    async def list(self, skip: int = 0, limit: int = 10):
        files = self.repo.list(skip, limit)
        total = self.repo.get_total_files()
        return files, total

    async def get(self, file_id):
        return self.repo.get(file_id)