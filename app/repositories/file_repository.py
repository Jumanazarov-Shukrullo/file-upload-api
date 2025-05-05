import hashlib
from sqlalchemy.orm import Session
from db.models import FileMeta
from schemas.file_schemas import FileMetaCreate

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_metadata(self, meta: FileMetaCreate):
        file = FileMeta(**meta.dict())
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def list(self, skip: int = 0, limit: int = 10):
        return self.db.query(FileMeta).offset(skip).limit(limit).all()

    def get(self, file_id):
        return self.db.query(FileMeta).filter(FileMeta.id == file_id).first()

    def get_total_files(self):
        return self.db.query(FileMeta).count()