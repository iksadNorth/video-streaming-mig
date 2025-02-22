import asyncio
import cv2

def get_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

async def extract_frame(video_path, output_path, target_frame):
    command = f'ffmpeg -i {video_path} -vf "select=eq(n\\,{target_frame})" -vsync vfr {output_path}'

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print(f"Extracted frame {target_frame}, saved at {output_path}")
    else:
        print(f"Error extracting frame: {stderr.decode()}")


# 여러 개의 프레임을 동시에 추출
async def extract_frame_parallel(id, num_thumbnail=10):
    video_path = f"static/{id}/src.mp4"
    output_path = f"static/{id}"
    
    total_frames = get_total_frames(video_path)
    
    iterator = range(num_thumbnail)
    iterator = (total_frames * (i / num_thumbnail) for i in iterator)
    iterator = (int(i) for i in iterator)
    tasks = [
        extract_frame(video_path, f"{output_path}/thumbnail_{idx}.jpg", i) 
        for idx, i in enumerate(iterator)
    ]
    
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(extract_frame_parallel('9202'))
