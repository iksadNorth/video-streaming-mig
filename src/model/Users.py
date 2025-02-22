from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.model.BaseModel import BaseModel


class Users(BaseModel):
    email = Column(String, unique=True, index=True)
    nickname = Column(String)
    bedge_src = Column(String)
    
    videos = relationship("Video", back_populates="publisher")
    comments = relationship("Comment", back_populates="publisher")
