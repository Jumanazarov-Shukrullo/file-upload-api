import fileinput

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from core.security import verify_token
from db.session import SessionLocal, Base, engine
from repositories.file_repository import FileRepository
from services.file_service import FileService
from schemas.file_schemas import FileMetaResponse, FileMetaListResponse

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=FileMetaResponse, dependencies=[Depends(verify_token)])
async def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    allowed = {"dcm", "jpg", "png", "pdf"}
    ext = file.filename.split('.')[-1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    repo = FileRepository(db)
    service = FileService(repo, db)
    meta = await service.upload(file)
    return FileMetaResponse(
        id=meta.id,
        filename=meta.filename,
        content_type=meta.content_type,
        url=meta.url,
        size=meta.size
    )


@router.get('/all-files', response_model=FileMetaListResponse, dependencies=[Depends(verify_token)])
async def get_all_files(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = FileRepository(db)
    service = FileService(repo, db)
    files, total = await service.list(skip, limit)
    converted_files = [
        FileMetaResponse(
            id=file.id,
            filename=file.filename,
            content_type=file.content_type,
            url=file.url,
            size=file.size
        ) for file in files
    ]
    return FileMetaListResponse(files=converted_files, total=total)


@router.get('/file/{file_id}', response_model=FileMetaResponse, dependencies=[Depends(verify_token)])
async def get_file(file_id, db: Session = Depends(get_db)):
    repo = FileRepository(db)
    service = FileService(repo, db)
    file = await service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail='File not found')
    return FileMetaResponse(
        id=file.id,
        filename=file.filename,
        content_type=file.content_type,
        url=file.url,
        size=file.size
    )
