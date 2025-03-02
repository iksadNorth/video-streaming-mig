from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qsl
from src.transaction.decorator import synchronized_method
from threading import RLock


class SeleniumUtils:
    def __init__(self, driver=None):
        self._driver = driver or self.get_new_driver()
        self.lock = RLock()
    
    def get_new_driver(self):
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")               # GUI 없이 실행
        chrome_options.add_argument("--disable-gpu")            # GPU 가속 비활성화
        chrome_options.add_argument("--no-sandbox")             # 샌드박스 모드 비활성화 (리눅스 환경에서 권장)
        chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화 (메모리 부족 방지)
        chrome_options.add_argument("--window-size=1920x1080")  # 창 크기 설정 (일부 웹사이트 대응)
        
        return webdriver.Chrome(options=chrome_options)
    
    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, value):
        raise ValueError("재정의 불가")
    
    def __del__(self):
        self.driver.quit()
    
    @synchronized_method
    def navigate(self, url):
        return self.driver.get(url)
    
    @synchronized_method
    def get_html(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')

class ScrollUtils(SeleniumUtils):
    def __init__(self, driver=None):
        super().__init__(driver)
    
    @synchronized_method
    def scrollY(self, dh):
        return self.driver.execute_script(f"""
            window.scrollBy(0, {dh});
            return window.scrollY;
        """)
    
    @synchronized_method
    def scroll_to_end_smoothly(self, dh=500):
        prev_height = self.driver.execute_script('return window.scrollY;')
        while True:
            if prev_height == ( new_height := self.scrollY(dh) ): break
            prev_height = new_height

class YoutubeUtils(SeleniumUtils):
    def __init__(self, driver=None):
        super().__init__(driver)
    
    def get_arr_video(self, soup):
        iterator = soup.select('ytd-video-renderer')
        iterator = (i.select('a[href]') for i in iterator)
        iterator = map(self.get_video_link, iterator)
        iterator = map(self.get_video_id, iterator)
        return iterator
    
    def get_video_link(self, arr_a):
        for tag_a in arr_a:
            link = tag_a.get('href')
            if not link.startswith('/watch'): continue
            return link
        else:
            return None
    
    def get_video_id(self, url):
        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        return params.get('v')
    
    def get_youtube_url(self, video_id):
        return f'https://www.youtube.com/watch?v={video_id}'
    
    
    def get_arr_shorts (self, soup):
        iterator = soup.select('ytm-shorts-lockup-view-model')
        iterator = (i.select('a[href]') for i in iterator)
        iterator = map(self.get_shorts_link, iterator)
        iterator = map(self.get_shorts_id, iterator)
        return iterator
    
    def get_shorts_link(self, arr_a):
        for tag_a in arr_a:
            link = tag_a.get('href')
            if not link.startswith('/shorts'): continue
            return link
        else:
            return None
    
    def get_shorts_id(self, url):
        return url.replace('/shorts/', '')
    
    def get_shorts_url(self, shorts_id):
        return f'https://www.youtube.com/shorts/{shorts_id}'


class CrawlingToolBox(SeleniumUtils):
    def __init__(self):
        super().__init__()
        self.scroll = ScrollUtils(self.driver)
        self.youtube = YoutubeUtils(self.driver)
    
    @synchronized_method
    def yield_video_id(self, url, max_num_scroll=1000):
        self.navigate(url)
    
        hash_table_id = set()
        for _ in range(max_num_scroll):
            soup = self.get_html()
            arr = self.youtube.get_arr_video(soup)
            for video_id in arr:
                if not video_id: continue
                if video_id in hash_table_id: continue
                hash_table_id.add(video_id)
                yield video_id
            self.scroll.scroll_to_end_smoothly(50)
    
    def yield_trending_video_id(self, max_num_scroll=1000):
        url = 'https://www.youtube.com/feed/trending'
        yield from self.yield_video_id(url, max_num_scroll)
    
    def yield_searched_video_id(self, keyword, max_num_scroll=1000):
        url = f'https://www.youtube.com/results?search_query={keyword}'
        yield from self.yield_video_id(url, max_num_scroll)
