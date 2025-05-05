from typing import List
from pydantic import BaseModel

class FileMetaCreate(BaseModel):
    id: str
    filename: str
    content_type: str
    url: str
    size: int

class FileMetaResponse(FileMetaCreate):
    pass

class FileMetaListResponse(BaseModel):
    files: List[FileMetaResponse]
    total: int