from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.model import BaseModel


class Comment(BaseModel):
    comment = Column(Text)
    
    publisher_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship("Users", back_populates="comments")
    
    video_id = Column(Integer, ForeignKey("video.id"))
    video = relationship("Video", back_populates="comments")
