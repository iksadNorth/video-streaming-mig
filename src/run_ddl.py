from src.video_streaming.db.database import engine
from src.video_streaming.model.BaseModel import BaseModel
from src.video_streaming.model import *

BaseModel.metadata.create_all(engine)
