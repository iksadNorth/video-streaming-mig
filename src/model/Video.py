from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pathlib import Path

from src.model.BaseModel import BaseModel
from src.config import config


ROOT_DIR = Path(config('video.path'))

class Video(BaseModel):
    file_path  = Column(String, unique=True)
    thumbnail_path  = Column(String, unique=True)
    title = Column(String)
    
    publisher_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship("Users", back_populates="videos")
    
    comments = relationship("Comment", back_populates="video")
