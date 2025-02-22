import os
import aiohttp
import asyncio
from pathlib import Path
from collections import deque


def pair(iterator, num=2):
    que = deque([], maxlen=num)
    for item in iterator:
        que.append(item)
        if len(que) < num: continue
        yield tuple(que)

class DownLoader:
    def __init__(self, output_file_path):
        self.output_file_path = Path(output_file_path)
        self.num = 10
        
    def get_output_file_path(self, video_id):
        dir_path = self.output_file_path / f'{video_id}'
        dir_path.mkdir(parents=True, exist_ok=True)
        
        return dir_path / 'src.mp4'
    
    def download_video(self, *args, **kwargs):
        async_task = self.async_download_video(*args, **kwargs)
        asyncio.run(async_task)

    # 커스터마이징 가능
    def get_part_file_path(self, video_id, suffix):
        return f'./parts/part_{video_id}_{suffix}.mp4'

    def add_range(self, headers, start='', end=''):
        if not start and not end: return headers
        headers = {k:v for k,v in headers.items()}
        headers['range'] = f'bytes={start}-{end}'
        return headers

    async def download_part(self, session, url, headers, part_num, video_id):
        range = headers.get('range')
        part_file_path = self.get_part_file_path(video_id, part_num)
        print(f"{part_file_path} 다운로드 시작: range|{range}")
        
        async with session.get(url, headers=headers) as response:
            print(f"{part_file_path} 응답 코드: ", response.status)
            with open(part_file_path, 'wb') as f:
                while chunk := await response.content.read(8192):
                    f.write(chunk)
        
        part_file_size = os.path.getsize(part_file_path)
        print(f"{part_file_path} 다운로드 완료, file size|{part_file_size}bytes")

    def merge_parts(self, video_id):
        output_file_path = self.get_output_file_path(video_id)
        
        # 기존 파일 삭제
        if output_file_path.exists():
            output_file_path.unlink()
        
        # 파일 병합
        with open(output_file_path, 'ab') as output_file:
            for num in range(self.num):
                part_file_path = self.get_part_file_path(video_id, num)
                with open(part_file_path, 'rb') as part_file:
                    output_file.write(part_file.read())
                os.remove(part_file_path)

    async def async_download_video(self, url, headers, video_id):
        async with aiohttp.ClientSession() as session:
            # 파일 전체 크기 확인
            async with session.head(url, headers=headers) as head_r:
                file_size = int(head_r.headers.get('Content-Length', 0))
            
            # 청크 크기 결정 및 header 생성
            parts = (int(part * (file_size+1)/self.num) for part in range(self.num+1))
            parts = pair(parts, 2)
            parts = (self.add_range(headers, start_byte, end_byte-1) for (start_byte, end_byte) in parts)

            # 비동기 요청 전송
            tasks = [
                self.download_part(session, url, header, idx, video_id) 
                for idx, header in enumerate(parts)
            ]
            await asyncio.gather(*tasks)
            self.merge_parts(video_id)


if __name__ == '__main__':    
    # 다운로더 설정
    downloader = DownLoader('./static')

    # 비동기 작업 실행
    headers = dict()
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    url = 'https://media.istockphoto.com/id/1868318353/ko/%EB%B9%84%EB%94%94%EC%98%A4/%EC%95%84%EC%B9%A8-%EC%82%B0%EB%A7%A5%EC%97%90%EC%84%9C-%ED%92%80%EB%B0%AD-%EC%96%B8%EB%8D%95%EC%9D%84-%EC%A1%B0%EA%B9%85%ED%95%98%EB%8A%94-%EC%97%AC%EC%9E%90.mp4?s=mp4-640x640-is&k=20&c=esvoXdkKGq101himBy4yQrAmMyHcJhRnpozpGdG0_pM='
    video_id = '0002'

    downloader.download_video(url, headers, video_id)
