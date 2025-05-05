from sqlalchemy import Column, String, Integer
from db.session import Base

class FileMeta(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    size = Column(Integer, nullable=False)