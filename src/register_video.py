from src.video_streaming.db.database import get_db
from src.video_streaming.model import Comment, Users, Video


for db in get_db():
    users = [
        Users(email='ROSÉ@noexist.com', nickname='ROSÉ', bedge_src='https://yt3.ggpht.com/qjsflFmyakGs5ekX8fPsDNfuKABx-yxIDrv-4ooPAFcZ6JUUpUPlue7g_d-VAk2YAiYR-0yr=s48-c-k-c0x00ffffff-no-rj'),
        Users(email='ChillVibesStation97@noexist.com', nickname='ChillVibesStation97', bedge_src='https://yt3.ggpht.com/2HOGEbS4V-u8tiQ6k6RmEbMa2oZJuigscOP1WomUbE6zJ1DvGWXCYS1z2koZUKJDURdVs_CwDw=s88-c-k-c0x00ffffff-no-rj'),
        Users(email='awgwef5ewedrfwe@noexist.com', nickname='awgwef5ewedrfwe', bedge_src='https://yt3.ggpht.com/Gs5RZTP9_2qb-2ItAy2ZZrKfSGAKoAUCNJjiG_sNkrdpvxrXKRni_8BMDxvgKdlf2FwdhyE=s88-c-k-c0x00ffffff-no-rj'),
        Users(email='ummmmmmum@noexist.com', nickname='ummmmmmum', bedge_src='https://yt3.ggpht.com/ytc/AIdro_lPZ02ITT9XKLBu5yfEZsM6uHNJ9VleTrmdVacaB69VPnM=s88-c-k-c0x00ffffff-no-rj'),
    ]
    comments = [
        Comment(
            comment='''
0:00        LANY - Anything 4 u
0:0:12      LANY - Anything 4 u
02:14       LANY - you!
2:14        LANY - you!
''',
            publisher=users[1],
        ),
        Comment(
            comment='''
진찌 행복 별거없네요 깨끗하게 씻고 창문열어놓고 포근한 이블속에서 좋아는 향수 뿌려주고 
이어폰끼고 들으니까 넘 행복한거같아요 진찌루
이거 읽으시는 분들도 오늘보다 더행복한 내일이었으면 좋겠어요
''',
            publisher=users[2],
        ),
        Comment(
            comment='''
아니 제가 좋아하는 가수 다 모아놓으면 당연히 좋을 수 밖에... 레이니, 콜플, 라우브 노래 진짜 좋아요 ㅠㅠ
''',
            publisher=users[3],
        ),
    ]
    
    video = Video(
        title='ROSÉ & Bruno Mars - APT. (Official Music Video)', 
        file_path='0001.mp4',
        publisher=users[0], 
        comments=comments, 
    )
    
    db.add(video)
