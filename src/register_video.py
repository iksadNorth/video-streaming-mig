from src.down_loader import DownLoader
from src.save_thumbnail import ThumbnailHandler
from src.db.database import get_db
from src.model import Video
from src.rules import PathRule
from sqlalchemy.orm import Session


class VideoRegister:
    def __init__(self, headers: dict = dict()):
        self.rule = PathRule()
        
        self.headers = headers
        self.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        
        self.downloader = DownLoader(self.rule)
        self.thumbnail_handler = ThumbnailHandler(self.rule)
    
    def get_video_id(self, db: Session, meta: dict = dict()):
        video = Video(**meta)
        db.add(video)
        db.flush()
        return video.id
    
    def download_video(self, url, video_id):
        self.downloader.download_video(url, self.headers, video_id)
    
    def get_thumbnail(self, video_id):
        self.thumbnail_handler.extract_frame_parallel(video_id)

    def rollback(self, video_entity, db: Session):
        self.rule.rm(video_entity.id)
        db.delete(video_entity)
        db.commit()

    def regist(self, url: str, meta: dict = dict()):
        # Pk값을 받아옴.
        video_id = None
        for db in get_db():
            video_id = self.get_video_id(db, meta)
        
        for db in get_db():
            # 업데이트를 위한 엔티티
            video_entity: Video = db.query(Video).filter(Video.id == video_id).first()
            
            try:
                self.download_video(url, video_entity.id)
                video_entity.file_path = self.rule.get_video_path(video_entity.id)
                
                self.get_thumbnail(video_entity.id)
                video_entity.thumbnail_path = self.rule.get_thumbnail_path(video_entity.id, 1)
            except:
                self.rollback(video_entity, db)
                continue


if __name__ == '__main__':
    # 썸네일 추출함. pk값에 대해 파일경로 업데이트 시킴
    url = 'https://media.istockphoto.com/id/1868318353/ko/%EB%B9%84%EB%94%94%EC%98%A4/%EC%95%84%EC%B9%A8-%EC%82%B0%EB%A7%A5%EC%97%90%EC%84%9C-%ED%92%80%EB%B0%AD-%EC%96%B8%EB%8D%95%EC%9D%84-%EC%A1%B0%EA%B9%85%ED%95%98%EB%8A%94-%EC%97%AC%EC%9E%90.mp4?s=mp4-640x640-is&k=20&c=esvoXdkKGq101himBy4yQrAmMyHcJhRnpozpGdG0_pM='
    meta = {
        'title': 'test_video',
    };
    register = VideoRegister()
    register.regist(url, meta)
