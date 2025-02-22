import os
import aiohttp
import asyncio

from src.video_streaming.utils.utils import pair


class DownLoader:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path
        self.num = 10
    
    def download_video(self, url, headers=dict()):
        async_task = self.async_download_video(url, headers)
        asyncio.run(async_task)

    # 커스터마이징 가능
    def get_part_file_path(self, suffix):
        return f'./parts/part_{suffix}.mp4'

    def add_range(self, headers, start='', end=''):
        if not start and not end: return headers
        headers = {k:v for k,v in headers.items()}
        headers['range'] = f'bytes={start}-{end}'
        return headers

    async def download_part(self, session, url, headers, part_num):
        range = headers.get('range')
        part_file_path = self.get_part_file_path(part_num)
        print(f"{part_file_path} 다운로드 시작: range|{range}")
        
        async with session.get(url, headers=headers) as response:
            print(f"{part_file_path} 응답 코드: ", response.status)
            with open(part_file_path, 'wb') as f:
                while chunk := await response.content.read(8192):
                    f.write(chunk)
        
        part_file_size = os.path.getsize(part_file_path)
        print(f"{part_file_path} 다운로드 완료, file size|{part_file_size}bytes")

    def merge_parts(self):
        # 기존 파일 삭제
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)
        
        # 파일 병합
        with open(self.output_file_path, 'ab') as output_file:
            for num in range(self.num):
                with open(self.get_part_file_path(num), 'rb') as part_file:
                    output_file.write(part_file.read())
                os.remove(self.get_part_file_path(num))

    async def async_download_video(self, url, headers):
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
                self.download_part(session, url, header, idx) 
                for idx, header in enumerate(parts)
            ]
            await asyncio.gather(*tasks)
            self.merge_parts()


if __name__ == '__main__':    
    # 비동기 작업 실행
    headers = dict()
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'

    url = 'https://media.istockphoto.com/id/1868318353/ko/%EB%B9%84%EB%94%94%EC%98%A4/%EC%95%84%EC%B9%A8-%EC%82%B0%EB%A7%A5%EC%97%90%EC%84%9C-%ED%92%80%EB%B0%AD-%EC%96%B8%EB%8D%95%EC%9D%84-%EC%A1%B0%EA%B9%85%ED%95%98%EB%8A%94-%EC%97%AC%EC%9E%90.mp4?s=mp4-640x640-is&k=20&c=esvoXdkKGq101himBy4yQrAmMyHcJhRnpozpGdG0_pM='
    downloader = DownLoader('./static/0001/src.mp4')
    downloader.download_video(url, headers)
