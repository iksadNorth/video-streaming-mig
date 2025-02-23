from pathlib import Path
from shutil import rmtree
from src.config import config


class PathRule():
    def __init__(self):
        self.output_file_path = Path(config('video.path'))
    
    '''
    리소스 파일 기준 상대적인 경로 정의
    '''
    @classmethod
    def get_container_path(cls, video_id: str):
        return f'{video_id}'
    
    @classmethod
    def get_video_path(cls, video_id: str):
        return f'{video_id}/src.mp4'
    
    @classmethod
    def get_thumbnail_path(cls, video_id, idx):
        return f"{video_id}/thumbnail_{idx}.jpg"
    
    
    '''
    절대적인 경로 정의. 디렉토리가 없다면 생성.
    '''
    def get_real_container_path(self, video_id: str):
        video_file_path = self.output_file_path / self.get_container_path(video_id)
        video_file_path.parent.mkdir(parents=True, exist_ok=True)
        return video_file_path
    
    def get_real_video_path(self, video_id: str):
        video_file_path = self.output_file_path / self.get_video_path(video_id)
        video_file_path.parent.mkdir(parents=True, exist_ok=True)
        return video_file_path

    def get_real_thumbnail_path(self, video_id, idx):
        thumbnail_file_path = self.output_file_path / self.get_thumbnail_path(video_id, idx)
        thumbnail_file_path.parent.mkdir(parents=True, exist_ok=True)
        return thumbnail_file_path
    
    '''
    특정 Video 경로 모두 삭제.
    '''
    def rm(self, video_id: str):
        target_dir = self.get_real_container_path(video_id)
        path = Path(target_dir)
        if path.exists() and path.is_dir():
            rmtree(path)


if __name__ == '__main__':
    print(PathRule.get_video_path('test_directory'))
    print(PathRule.get_thumbnail_path('test_directory', 1))
    
    rule = PathRule()
    print(rule.get_real_video_path('test_directory'))
    print(rule.get_real_thumbnail_path('test_directory', 1))
    
    rule.rm('test_directory')
