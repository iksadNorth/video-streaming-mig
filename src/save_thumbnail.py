import asyncio
from src.rules import PathRule
import json
from functools import partial


class ThumbnailHandler():
    def __init__(self, path_rules: PathRule):
        self.path_rules = path_rules
    
    @classmethod
    def get_thumbnail_path(self, video_id, idx):
        return f"{video_id}/thumbnail_{idx}.jpg"
    
    @classmethod
    def get_video_path(self, video_id):
        return f"{video_id}/src.mp4"
    
    async def get_total_duration(self, video_path):
        cmd = f"ffprobe -v error -select_streams v:0 -show_entries format=duration -of json {video_path}"
        process = await asyncio.subprocess.create_subprocess_shell(
            cmd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        duration = json.loads(stdout.decode())["format"]["duration"]
        
        return float(duration)

    async def aysnc_extract_frame(self, video_path, output_path, seek_time):
        command = f'ffmpeg -ss {seek_time} -i {video_path} -frames:v 1 {output_path}'

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"Extracted Seek Time {seek_time}, saved at {output_path}")
        else:
            print(f"Error extracting Seek Time: {stderr.decode()}")

    # 여러 개의 프레임을 동시에 추출
    async def aysnc_extract_frame_parallel(self, id, num_thumbnail=10):
        video_path = self.path_rules.get_real_video_path(id)
        output_path = partial(self.path_rules.get_real_thumbnail_path, video_id=id)
        
        total_duration = await self.get_total_duration(video_path)
        
        iterator = range(num_thumbnail)
        iterator = (total_duration * (i / num_thumbnail) for i in iterator)
        iterator = (int(i) for i in iterator)
        tasks = [
            self.aysnc_extract_frame(video_path, output_path(idx=idx), i) 
            for idx, i in enumerate(iterator)
        ]
        
        await asyncio.gather(*tasks)
    
    def extract_frame_parallel(self, *args, **kwargs):
        asyncio.run(self.aysnc_extract_frame_parallel(*args, **kwargs))


if __name__ == '__main__':
    # 경로 규칙
    rule = PathRule()
    
    handler = ThumbnailHandler(rule)
    handler.extract_frame_parallel('0002')
