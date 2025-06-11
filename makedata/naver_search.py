import requests
import json
import urllib.parse
from bs4 import BeautifulSoup
import time
import re
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random

class NaverSearchAPI:
    def __init__(self, client_id, client_secret):
        """
        네이버 검색 API 클래스 초기화
        
        Args:
            client_id (str): 네이버 개발자센터에서 발급받은 Client ID
            client_secret (str): 네이버 개발자센터에서 발급받은 Client Secret
        """
        self.client_id = "nML9kslg3kN6ObjrujI3"
        self.client_secret = "UynDCaMJCt"
        self.base_url = "https://openapi.naver.com/v1/search"
    
    def _make_request(self, endpoint, query, display=10, start=1, sort="sim"):
        """
        네이버 API에 요청을 보내는 공통 메서드
        
        Args:
            endpoint (str): API 엔드포인트 (blog, news, book, etc.)
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: API 응답 결과
        """
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류가 발생했습니다: {e}")
            return None
    
    def search_blog(self, query, display=10, start=1, sort="sim"):
        """
        블로그 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 블로그 검색 결과
        """
        return self._make_request("blog", query, display, start, sort)
    
    def search_news(self, query, display=10, start=1, sort="sim"):
        """
        뉴스 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 뉴스 검색 결과
        """
        return self._make_request("news", query, display, start, sort)
    
    def search_book(self, query, display=10, start=1, sort="sim"):
        """
        책 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 책 검색 결과
        """
        return self._make_request("book", query, display, start, sort)
    
    def search_encyc(self, query, display=10, start=1):
        """
        백과사전 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
        
        Returns:
            dict: 백과사전 검색 결과
        """
        return self._make_request("encyc", query, display, start)
    
    def search_movie(self, query, display=10, start=1):
        """
        영화 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
        
        Returns:
            dict: 영화 검색 결과
        """
        return self._make_request("movie", query, display, start)
    
    def search_cafearticle(self, query, display=10, start=1, sort="sim"):
        """
        카페글 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 카페글 검색 결과
        """
        return self._make_request("cafearticle", query, display, start, sort)
    
    def search_kin(self, query, display=10, start=1, sort="sim"):
        """
        지식iN 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 지식iN 검색 결과
        """
        return self._make_request("kin", query, display, start, sort)
    
    def search_local(self, query, display=5, start=1, sort="random"):
        """
        지역 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~5)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (random: 정확도순, comment: 업체리뷰개수순)
        
        Returns:
            dict: 지역 검색 결과
        """
        return self._make_request("local", query, display, start, sort)
    
    def search_image(self, query, display=10, start=1, sort="sim", filter="all"):
        """
        이미지 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
            filter (str): 필터 옵션 (all: 전체, large: 큰 이미지, medium: 중간 이미지, small: 작은 이미지)
        
        Returns:
            dict: 이미지 검색 결과
        """
        url = f"{self.base_url}/image"
        
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort,
            "filter": filter
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류가 발생했습니다: {e}")
            return None

class NaverBlogSearchAPI:
    def __init__(self, client_id=None, client_secret=None):
        """
        네이버 블로그 검색 API 클래스 초기화
        
        Args:
            client_id (str): 네이버 개발자센터에서 발급받은 Client ID
            client_secret (str): 네이버 개발자센터에서 발급받은 Client Secret
        """
        self.client_id = "nML9kslg3kN6ObjrujI3"
        self.client_secret = "UynDCaMJCt"
        self.base_url = "https://openapi.naver.com/v1/search/blog"
        
        # 다양한 User-Agent 목록
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    def _get_random_user_agent(self):
        """랜덤 User-Agent 반환"""
        return random.choice(self.user_agents)
    
    def _random_delay(self, min_delay=1, max_delay=3):
        """랜덤 지연 시간"""
        delay = random.uniform(min_delay, max_delay)
        print(f"   잠시 대기 중... ({delay:.1f}초)")
        time.sleep(delay)
    
    def search_blog(self, query, display=10, start=1, sort="sim"):
        """
        블로그 검색
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (1~100)
            start (int): 검색 시작 위치 (1~1000)
            sort (str): 정렬 옵션 (sim: 정확도순, date: 날짜순)
        
        Returns:
            dict: 블로그 검색 결과
        """
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
            "User-Agent": self._get_random_user_agent(),
            "Accept": "application/json",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류가 발생했습니다: {e}")
            return None
    
    def get_blog_content_with_selenium(self, blog_url, max_retries=3):
        """
        Selenium을 사용하여 블로그 URL에서 본문 내용을 추출 (스텔스 모드)
        """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 랜덤 User-Agent 사용
        user_agent = self._get_random_user_agent()
        options.add_argument(f'--user-agent={user_agent}')
        
        # 추가 스텔스 옵션들
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # 이미지 로딩 비활성화로 속도 향상
        
        # 윈도우 크기 랜덤화
        window_sizes = ['1920,1080', '1366,768', '1440,900', '1536,864']
        options.add_argument(f'--window-size={random.choice(window_sizes)}')

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # WebDriver 감지 방지 스크립트
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko']})")
            
            # 랜덤 지연 후 페이지 로드
            self._random_delay(1, 2)
            driver.get(blog_url)
            
            # 페이지 로딩 완료까지 랜덤 대기
            loading_delay = random.uniform(2, 4)
            time.sleep(loading_delay)
            
            # 사람처럼 행동 시뮬레이션
            self._simulate_human_behavior(driver)
            
            # 네이버 블로그인 경우 iframe 처리
            if 'blog.naver.com' in blog_url:
                return self._extract_naver_blog_selenium_enhanced(driver, blog_url)
            
            # 티스토리 블로그 본문 추출
            content = self._extract_tistory_content_selenium(driver)
            if content:
                return content

            # 일반적인 블로그 본문 추출
            content = self._extract_general_content_selenium(driver)
            if content:
                return content

            return {"title": "제목을 가져올 수 없음", "content": "본문을 가져올 수 없습니다."}
            
        except Exception as e:
            print(f"Selenium을 사용한 블로그 내용 가져오기 실패: {e}")
            return {"title": "제목을 가져올 수 없음", "content": "본문을 가져올 수 없습니다."}
        finally:
            try:
                driver.quit()
            except:
                pass

    def _simulate_human_behavior(self, driver):
        """사람처럼 행동하는 시뮬레이션"""
        try:
            # 랜덤 스크롤
            scroll_count = random.randint(1, 3)
            for _ in range(scroll_count):
                scroll_amount = random.randint(200, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # 페이지 상단으로 돌아가기
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(0.5, 1))
            
        except Exception:
            pass  # 스크롤 실패해도 계속 진행

    def _scroll_for_more_content(self, driver, display):
        """더 많은 블로그를 찾기 위해 페이지 스크롤"""
        try:
            # 페이지 스크롤 반복
            for _ in range(display - 5):
                # 스크롤 다운
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(random.uniform(0.5, 1))
            
            # 스크롤 마지막 위치로 이동
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.5, 1))
            
        except Exception as e:
            print(f"더 많은 블로그를 찾기 위해 페이지 스크롤 실패: {e}")

    def _extract_naver_blog_selenium_enhanced(self, driver, blog_url):
        """향상된 네이버 블로그 Selenium 추출"""
        try:
            # 네이버 블로그는 iframe을 사용하므로 iframe으로 전환
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
            title = "제목을 찾을 수 없음"
            content = ""
            
            # 메인 페이지에서 제목 찾기
            title_selectors = [
                '.blog_title',
                '.se-title-text', 
                '.pcol1 .title_area .title',
                'h1',
                'h2',
                '.title'
            ]
            
            for selector in title_selectors:
                try:
                    title_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if title_elem and title_elem.text.strip():
                        title = title_elem.text.strip()
                        break
                except:
                    continue
            
            # iframe에서 본문 찾기
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    time.sleep(2)
                    
                    # 다양한 선택자로 본문 찾기
                    content_selectors = [
                        '.se-main-container',
                        '.se-component-content',
                        '.se-text',
                        '.se-text-paragraph',
                        '.post-view',
                        '.post_ct',
                        '.blog_view',
                        '.contents_style',
                        'body'
                    ]
                    
                    for selector in content_selectors:
                        try:
                            content_elem = driver.find_element(By.CSS_SELECTOR, selector)
                            if content_elem:
                                content_text = content_elem.text.strip()
                                if len(content_text) > 50:  # 충분한 내용이 있는 경우
                                    content = content_text
                                    break
                        except:
                            continue
                    
                    if content:
                        break
                        
                    driver.switch_to.default_content()
                    
                except Exception as e:
                    driver.switch_to.default_content()
                    continue
            
            # iframe에서 찾지 못한 경우 메인 페이지에서 찾기
            if not content:
                try:
                    # 페이지 전체 텍스트 가져오기
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    if len(body_text) > 100:
                        # 불필요한 텍스트 제거하고 의미있는 부분만 추출
                        lines = body_text.split('\n')
                        meaningful_lines = []
                        for line in lines:
                            line = line.strip()
                            if (len(line) > 10 and 
                                not line.startswith('http') and 
                                '댓글' not in line and 
                                '공감' not in line and
                                '이웃' not in line):
                                meaningful_lines.append(line)
                        
                        if meaningful_lines:
                            content = '\n'.join(meaningful_lines[:20])  # 처음 20줄만
                except:
                    pass
            
            if not content:
                content = "본문을 추출할 수 없습니다."
            
            return {"title": title, "content": self._clean_text(content)}
            
        except Exception as e:
            print(f"네이버 블로그 향상된 Selenium 추출 중 오류: {e}")
            return {"title": "제목을 가져올 수 없음", "content": "본문을 가져올 수 없습니다."}

    def _extract_naver_blog_content_selenium(self, driver):
        """기본 네이버 블로그 Selenium 추출 (호환성을 위해 유지)"""
        return self._extract_naver_blog_selenium_enhanced(driver, driver.current_url)

    def _extract_tistory_content_selenium(self, driver):
        """Selenium을 사용하여 티스토리 블로그 본문 추출"""
        try:
            title = driver.find_element(By.CSS_SELECTOR, '.entry-title').text
            content = driver.find_element(By.CSS_SELECTOR, '.entry-content').text
            return {"title": title, "content": self._clean_text(content)}
        except Exception as e:
            print(f"티스토리 블로그 Selenium 추출 중 오류: {e}")
            return None

    def _extract_general_content_selenium(self, driver):
        """Selenium을 사용하여 일반적인 블로그 본문 추출"""
        try:
            title = driver.find_element(By.TAG_NAME, 'h1').text
            content = driver.find_element(By.TAG_NAME, 'body').text
            return {"title": title, "content": self._clean_text(content)}
        except Exception as e:
            print(f"일반 블로그 Selenium 추출 중 오류: {e}")
            return None

    def _clean_text(self, text):
        """텍스트 정리"""
        if not text:
            return "본문을 가져올 수 없습니다."
        
        # 연속된 공백과 줄바꿈 정리
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # CSV 저장을 위해 따옴표와 쉼표 처리
        text = text.replace('"', '""')  # CSV에서 따옴표 이스케이프
        
        return text.strip()
    
    def save_to_csv(self, search_query, results, filename="blog_search_results.csv"):
        """
        검색 결과를 CSV 파일에 저장
        
        Args:
            search_query (str): 검색어
            results (list): 검색 결과 리스트
            filename (str): 저장할 파일명
        """
        # CSV 파일이 존재하는지 확인
        file_exists = os.path.isfile(filename)
        
        try:
            with open(filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['검색어', '본문내용', '제목', '블로거', '작성일', '링크']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # 파일이 새로 생성되는 경우 헤더 작성
                if not file_exists:
                    writer.writeheader()
                
                # 검색 결과 저장
                for result in results:
                    if result.get('content') and result['content'].get('content'):
                        content_text = result['content']['content']
                    else:
                        content_text = result.get('description', "본문을 가져올 수 없습니다.")
                    
                    writer.writerow({
                        '검색어': search_query,
                        '본문내용': content_text,
                        '제목': result.get('title', ''),
                        '블로거': result.get('bloggername', ''),
                        '작성일': result.get('postdate', ''),
                        '링크': result.get('link', '')
                    })
            
            print(f"\n✅ 검색 결과가 '{filename}' 파일에 저장되었습니다.")
            return filename
            
        except Exception as e:
            print(f"❌ CSV 파일 저장 중 오류가 발생했습니다: {e}")
            return None
    
    def search_and_get_content(self, query, display=5, sort="sim", get_content=True, save_csv=True):
        """
        블로그 검색 후 본문 내용까지 가져오기 (개선된 버전 - 대량 수집 지원)
        
        Args:
            query (str): 검색어
            display (int): 검색 결과 출력 건수 (최대 1000개까지 지원)
            sort (str): 정렬 옵션
            get_content (bool): 본문 내용을 가져올지 여부
            save_csv (bool): CSV 파일로 저장할지 여부
        
        Returns:
            list: 블로그 검색 결과와 본문 내용
        """
        print(f"\n=== '{query}' 블로그 검색 결과 (API 사용) ===")
        
        all_results = []
        collected_count = 0
        start_position = 1
        
        # API는 한 번에 최대 100개까지만 가져올 수 있으므로 여러 번 호출
        while collected_count < display:
            # 이번 호출에서 가져올 개수 계산
            current_display = min(100, display - collected_count)
            
            print(f"API 호출 {(start_position-1)//100 + 1}: {start_position}~{start_position + current_display - 1}번째 결과 수집 중...")
            
            # 블로그 검색
            search_results = self.search_blog(query, current_display, start_position, sort=sort)
            
            if not search_results or not search_results.get('items'):
                print(f"더 이상 검색 결과가 없습니다. (총 {collected_count}개 수집)")
                break
            
            current_items = search_results['items']
            print(f"이번 호출에서 {len(current_items)}개 블로그 발견")
            
            # 결과 처리
            for i, item in enumerate(current_items, collected_count + 1):
                blog_info = {
                    'rank': i,
                    'title': item.get('title', '제목 없음'),
                    'description': item.get('description', '설명 없음'),
                    'link': item.get('link', ''),
                    'bloggername': item.get('bloggername', '알 수 없음'),
                    'postdate': item.get('postdate', '날짜 없음'),
                    'content': None
                }
                
                print(f"{i}. {blog_info['title']}")
                print(f"   블로거: {blog_info['bloggername']}")
                print(f"   작성일: {blog_info['postdate']}")
                print(f"   링크: {blog_info['link']}")
                print(f"   요약: {blog_info['description']}")
                
                if get_content and blog_info['link']:
                    print("   본문 가져오는 중...")
                    content_data = self.get_blog_content_with_selenium(blog_info['link'])
                    blog_info['content'] = content_data
                    
                    if content_data and content_data.get('content'):
                        print(f"   본문 미리보기: {content_data['content'][:100]}...")
                    else:
                        print("   본문을 가져올 수 없습니다.")
                    
                    # 요청 간격 조절 (너무 빠른 요청 방지) - 랜덤 지연
                    if i < display:  # 마지막이 아닌 경우에만
                        self._random_delay(1, 3)  # API는 더 빠르게
                
                print("-" * 60)
                all_results.append(blog_info)
                collected_count += 1
                
                # 목표 개수에 도달하면 중단
                if collected_count >= display:
                    break
            
            # 다음 페이지 준비
            start_position += current_display
            
            # API 호출 간 지연 (서버 부하 방지)
            if collected_count < display and len(current_items) == current_display:
                print("다음 페이지 준비 중...")
                self._random_delay(1, 2)
            else:
                # 더 이상 결과가 없으면 중단
                break
        
        print(f"\n총 {len(all_results)}개의 블로그 수집 완료!")
        
        # CSV 파일로 저장
        if save_csv and all_results:
            self.save_to_csv(query, all_results)
        
        return all_results

    def search_blog_without_api(self, query, display=5):
        """
        API 없이 네이버 블로그 검색 페이지를 직접 크롤링
        """
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 랜덤 User-Agent 사용
        user_agent = self._get_random_user_agent()
        options.add_argument(f'--user-agent={user_agent}')
        
        # 추가 스텔스 옵션들
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        
        # 윈도우 크기 랜덤화
        window_sizes = ['1920,1080', '1366,768', '1440,900', '1536,864']
        options.add_argument(f'--window-size={random.choice(window_sizes)}')

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # WebDriver 감지 방지 스크립트
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko']})")
            
            blog_results = []
            seen_links = set()
            page = 1
            
            # 여러 페이지에서 블로그 수집
            while len(blog_results) < display and page <= 10:  # 최대 10페이지까지
                # 페이지별 검색 URL (start 파라미터로 페이지네이션)
                start_num = (page - 1) * 10 + 1
                search_url = f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}&start={start_num}"
                
                print(f"   페이지 {page} 검색 중... (목표: {display}개, 현재: {len(blog_results)}개)")
                self._random_delay(1, 2)
                driver.get(search_url)
                
                # 페이지 로딩 대기
                loading_delay = random.uniform(3, 5)
                time.sleep(loading_delay)
                
                # 사람처럼 행동 시뮬레이션
                self._simulate_human_behavior(driver)
                
                # 페이지 끝까지 스크롤하여 모든 콘텐츠 로드
                self._scroll_to_load_all_content(driver)
                
                # 현재 페이지에서 블로그 링크 찾기
                page_links = self._extract_blog_links_from_page(driver, seen_links)
                
                if not page_links:
                    print(f"   페이지 {page}에서 새로운 블로그를 찾지 못했습니다.")
                    break
                
                # 결과에 추가
                for link_info in page_links:
                    if len(blog_results) >= display:
                        break
                    blog_results.append(link_info)
                    print(f"   블로그 {len(blog_results)}: {link_info['title'][:50]}...")
                
                page += 1
                
                # 페이지 간 지연
                if len(blog_results) < display and page <= 10:
                    self._random_delay(2, 4)
            
            print(f"   총 {len(blog_results)}개 블로그 수집 완료!")
            return blog_results
            
        except Exception as e:
            print(f"네이버 검색 페이지 크롤링 실패: {e}")
            return []
        finally:
            try:
                driver.quit()
            except:
                pass

    def _scroll_to_load_all_content(self, driver):
        """페이지 끝까지 스크롤하여 모든 콘텐츠 로드"""
        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_count = 0
            max_scrolls = 10  # 최대 스크롤 횟수
            
            while scroll_count < max_scrolls:
                # 페이지 끝까지 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 2))
                
                # 새로운 높이 확인
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                # 더 이상 로드할 콘텐츠가 없으면 중단
                if new_height == last_height:
                    break
                    
                last_height = new_height
                scroll_count += 1
                
                # 중간중간 스크롤 (더 자연스럽게)
                for _ in range(3):
                    scroll_position = random.randint(100, new_height - 100)
                    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                    time.sleep(random.uniform(0.3, 0.7))
                    
        except Exception as e:
            print(f"스크롤 중 오류: {e}")

    def _extract_blog_links_from_page(self, driver, seen_links):
        """현재 페이지에서 블로그 링크 추출"""
        page_results = []
        
        try:
            # 다양한 방법으로 블로그 링크 찾기
            selectors = [
                "a[href*='blog.naver.com']",
                "a[href*='blog.naver.com/PostView']",
                "a[href*='blog.naver.com'][href*='/22']",  # 222, 223 등
                ".blog_area a",
                ".total_area a[href*='blog.naver.com']",
                ".lst_total a[href*='blog.naver.com']"
            ]
            
            all_links = []
            for selector in selectors:
                try:
                    links = driver.find_elements(By.CSS_SELECTOR, selector)
                    all_links.extend(links)
                except:
                    continue
            
            print(f"   총 {len(all_links)}개 링크 발견")
            
            for link in all_links:
                try:
                    href = link.get_attribute('href')
                    if not href or href in seen_links:
                        continue
                    
                    # 블로그 포스트 링크 필터링 (조건 대폭 완화)
                    if (href and 'blog.naver.com' in href and 
                        # 더 관대한 조건들
                        (('/223' in href) or ('/222' in href) or ('/221' in href) or ('/220' in href) or
                         ('/PostView.naver' in href) or ('/post/' in href) or
                         ('logNo=' in href) or ('blogId=' in href) or
                         (href.count('/') >= 4 and not href.endswith('.naver') and 
                          not 'prologue' in href and not 'category' in href))):
                        
                        seen_links.add(href)
                        
                        # 제목 추출 (더 적극적으로)
                        title = self._extract_title_from_link(link)
                        
                        if title and len(title) > 1:  # 조건 더욱 완화
                            page_results.append({
                                'title': title,
                                'link': href,
                                'description': "설명 없음",
                                'bloggername': "알 수 없음", 
                                'postdate': "날짜 없음"
                            })
                            
                except Exception as e:
                    continue
            
            return page_results
            
        except Exception as e:
            print(f"블로그 링크 추출 중 오류: {e}")
            return []

    def _extract_title_from_link(self, link):
        """링크에서 제목 추출 (개선된 버전)"""
        try:
            # 1. 링크 텍스트에서 직접 추출
            title = link.text.strip()
            if title and len(title) > 3:
                return self._clean_title(title)
            
            # 2. 부모 요소들에서 제목 찾기 (더 적극적으로)
            current = link
            for level in range(8):  # 8레벨까지 확장
                try:
                    current = current.find_element(By.XPATH, "..")
                    parent_text = current.text.strip()
                    
                    if parent_text and len(parent_text) > 3:
                        lines = parent_text.split('\n')
                        for line in lines:
                            line = line.strip()
                            # 더 관대한 제목 조건
                            if (len(line) > 2 and len(line) < 300 and 
                                not line.startswith('http') and
                                not line.startswith('www') and
                                '블로그' not in line[:10] and
                                '네이버' not in line[:10]):
                                return self._clean_title(line)
                except:
                    break
            
            # 3. 주변 요소에서 제목 찾기
            try:
                # 형제 요소들 확인
                siblings = current.find_elements(By.XPATH, "../*")
                for sibling in siblings:
                    sibling_text = sibling.text.strip()
                    if (sibling_text and len(sibling_text) > 3 and len(sibling_text) < 200 and
                        not sibling_text.startswith('http')):
                        return self._clean_title(sibling_text)
            except:
                pass
            
            # 4. URL에서 추출
            href = link.get_attribute('href')
            if href:
                url_parts = href.split('/')
                if len(url_parts) > 3:
                    blog_id = url_parts[3] if len(url_parts) > 3 else "unknown"
                    return f"블로그 포스트 - {blog_id}"
            
            return "블로그 포스트"
            
        except Exception as e:
            return "블로그 포스트"

    def _clean_title(self, title):
        """제목 정리"""
        if not title:
            return "블로그 포스트"
        
        # 첫 번째 줄만 사용
        title = title.split('\n')[0].strip()
        
        # HTML 태그 제거
        title = title.replace('<b>', '').replace('</b>', '')
        title = title.replace('<em>', '').replace('</em>', '')
        title = title.replace('...', '').strip()
        
        # 특수 문자 정리
        title = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title if len(title) > 1 else "블로그 포스트"

    def search_and_get_content_without_api(self, query, display=5, get_content=True, save_csv=True):
        """
        API 없이 블로그 검색 후 본문 내용까지 가져오기
        """
        print(f"\n=== '{query}' 블로그 검색 결과 (API 미사용) ===")
        
        # 네이버 검색 페이지에서 블로그 결과 가져오기
        search_results = self.search_blog_without_api(query, display)
        
        if not search_results:
            print("검색 결과가 없습니다.")
            return []
        
        results = []
        print(f"총 {len(search_results)}개의 블로그를 찾았습니다.")
        print("-" * 60)
        
        # 검색 결과 순서 랜덤화 (패턴 숨기기)
        random.shuffle(search_results)
        
        for i, item in enumerate(search_results, 1):
            blog_info = {
                'rank': i,
                'title': item.get('title', '제목 없음'),
                'description': item.get('description', '설명 없음'),
                'link': item.get('link', ''),
                'bloggername': item.get('bloggername', '알 수 없음'),
                'postdate': item.get('postdate', '날짜 없음'),
                'content': None
            }
            
            print(f"{i}. {blog_info['title']}")
            print(f"   블로거: {blog_info['bloggername']}")
            print(f"   작성일: {blog_info['postdate']}")
            print(f"   링크: {blog_info['link']}")
            print(f"   요약: {blog_info['description']}")
            
            if get_content and blog_info['link']:
                print("   본문 가져오는 중...")
                
                # 검색과 크롤링 사이에 더 긴 지연 (자연스러운 패턴)
                self._random_delay(5, 10)
                
                content_data = self.get_blog_content_with_selenium(blog_info['link'])
                blog_info['content'] = content_data
                
                if content_data and content_data.get('content'):
                    print(f"   본문 미리보기: {content_data['content'][:100]}...")
                else:
                    print("   본문을 가져올 수 없습니다.")
                
                # 블로그 간 간격 (마지막이 아닌 경우에만)
                if i < len(search_results):
                    self._random_delay(3, 8)  # 더 긴 지연
            
            print("-" * 60)
            results.append(blog_info)
        
        # CSV 파일로 저장
        if save_csv and results:
            self.save_to_csv(query, results, "blog_search_results_no_api.csv")
        
        return results

def print_search_results(results, search_type):
    """
    검색 결과를 보기 좋게 출력하는 함수
    
    Args:
        results (dict): API 검색 결과
        search_type (str): 검색 타입
    """
    if not results:
        print("검색 결과가 없습니다.")
        return
    
    print(f"\n=== {search_type} 검색 결과 ===")
    print(f"총 검색 결과: {results.get('total', 0)}건")
    print(f"현재 페이지: {results.get('start', 0)}~{results.get('start', 0) + len(results.get('items', [])) - 1}")
    print("-" * 50)
    
    for i, item in enumerate(results.get('items', []), 1):
        print(f"{i}. {item.get('title', '제목 없음')}")
        if 'description' in item:
            print(f"   설명: {item['description']}")
        if 'link' in item:
            print(f"   링크: {item['link']}")
        if 'bloggername' in item:
            print(f"   블로거: {item['bloggername']}")
        if 'postdate' in item:
            print(f"   작성일: {item['postdate']}")
        if 'author' in item:
            print(f"   저자: {item['author']}")
        if 'publisher' in item:
            print(f"   출판사: {item['publisher']}")
        if 'pubdate' in item:
            print(f"   출간일: {item['pubdate']}")
        if 'address' in item:
            print(f"   주소: {item['address']}")
        if 'telephone' in item:
            print(f"   전화번호: {item['telephone']}")
        print()

def main():
    """
    메인 함수 - 블로그 검색 및 본문 크롤링
    """
    # API 클래스 인스턴스 생성
    blog_api = NaverBlogSearchAPI()
    
    print("=== 네이버 블로그 검색 및 본문 크롤링 ===\n")
    
    # 검색 방법 선택
    print("검색 방법을 선택하세요:")
    print("1. API 사용 (빠르지만 로그가 남음)")
    print("2. 직접 크롤링 (느리지만 더 안전함)")
    
    while True:
        choice = input("선택 (1 또는 2): ").strip()
        if choice in ['1', '2']:
            break
        print("1 또는 2를 입력해주세요.")
    
    # 검색어 입력 (최대 10개)
    print("\n검색어를 입력하세요 (최대 10개까지 가능):")
    print("- 검색어를 하나씩 입력하고 Enter를 누르세요")
    print("- 입력을 마치려면 빈 줄에서 Enter를 누르세요")
    print("- 또는 쉼표(,)로 구분하여 한 번에 입력할 수도 있습니다")
    
    search_queries = []
    
    # 첫 번째 입력 받기
    first_input = input("검색어 입력: ").strip()
    
    if not first_input:
        print("검색어를 입력해주세요.")
        return
    
    # 쉼표로 구분된 여러 검색어인지 확인
    if ',' in first_input:
        # 쉼표로 구분된 검색어들 처리
        queries = [q.strip() for q in first_input.split(',') if q.strip()]
        search_queries.extend(queries[:10])  # 최대 10개까지만
        print(f"입력된 검색어: {search_queries}")
    else:
        # 단일 검색어로 시작
        search_queries.append(first_input)
        
        # 추가 검색어 입력 받기
        for i in range(2, 11):  # 2번째부터 10번째까지
            query = input(f"검색어 {i} (Enter로 완료): ").strip()
            if not query:
                break
            search_queries.append(query)
    
    if not search_queries:
        print("검색어를 입력해주세요.")
        return
    
    print(f"\n총 {len(search_queries)}개의 검색어가 입력되었습니다:")
    for i, query in enumerate(search_queries, 1):
        print(f"{i}. {query}")
    
    # 검색할 블로그 개수 선택
    print("\n각 검색어당 검색할 블로그 개수를 선택하세요:")
    if choice == '1':  # API 사용
        print("1. 10개 (빠름)")
        print("2. 50개 (보통)")
        print("3. 100개 (많음)")
        print("4. 200개 (대량)")
        print("5. 직접 입력")
        
        while True:
            count_choice = input("선택 (1-5): ").strip()
            if count_choice in ['1', '2', '3', '4', '5']:
                break
            print("1, 2, 3, 4, 또는 5를 입력해주세요.")
        
        # 블로그 개수 설정
        if count_choice == '1':
            display_count = 10
        elif count_choice == '2':
            display_count = 50
        elif count_choice == '3':
            display_count = 100
        elif count_choice == '4':
            display_count = 200
        else:  # count_choice == '5'
            while True:
                try:
                    display_count = int(input("검색할 블로그 개수를 입력하세요 (1-1000): "))
                    if 1 <= display_count <= 1000:
                        break
                    else:
                        print("1부터 1000 사이의 숫자를 입력해주세요.")
                except ValueError:
                    print("숫자를 입력해주세요.")
    else:  # 직접 크롤링
        print("1. 5개 (빠름)")
        print("2. 10개 (보통)")
        print("3. 20개 (느림)")
        print("4. 직접 입력")
        
        while True:
            count_choice = input("선택 (1-4): ").strip()
            if count_choice in ['1', '2', '3', '4']:
                break
            print("1, 2, 3, 또는 4를 입력해주세요.")
        
        # 블로그 개수 설정
        if count_choice == '1':
            display_count = 5
        elif count_choice == '2':
            display_count = 10
        elif count_choice == '3':
            display_count = 20
        else:  # count_choice == '4'
            while True:
                try:
                    display_count = int(input("검색할 블로그 개수를 입력하세요 (1-50): "))
                    if 1 <= display_count <= 50:
                        break
                    else:
                        print("1부터 50 사이의 숫자를 입력해주세요.")
                except ValueError:
                    print("숫자를 입력해주세요.")
    
    # 예상 소요 시간 계산 및 안내
    total_blogs = len(search_queries) * display_count
    if choice == '2':  # 직접 크롤링
        estimated_time = total_blogs * 10  # 블로그당 약 10초
        print(f"\n⏰ 예상 소요 시간: 약 {estimated_time//60}분 {estimated_time%60}초")
        print("💡 직접 크롤링은 안전하지만 시간이 오래 걸립니다.")
    else:  # API 사용
        estimated_time = total_blogs * 3  # 블로그당 약 3초
        print(f"\n⏰ 예상 소요 시간: 약 {estimated_time//60}분 {estimated_time%60}초")
    
    print(f"📊 총 수집 예정 블로그: {total_blogs}개 ({len(search_queries)}개 검색어 × {display_count}개)")
    
    confirm = input("계속 진행하시겠습니까? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '예', 'ㅇ']:
        print("작업을 취소했습니다.")
        return
    
    # 각 검색어에 대해 순차적으로 검색 실행
    all_results = []
    total_collected = 0
    
    for i, search_query in enumerate(search_queries, 1):
        print(f"\n{'='*60}")
        print(f"🔍 검색 진행: {i}/{len(search_queries)} - '{search_query}'")
        print(f"{'='*60}")
        
        if choice == '1':
            print(f"API를 사용하여 '{search_query}' 검색 중... ({display_count}개)")
            results = blog_api.search_and_get_content(
                query=search_query,
                display=display_count,
                sort="sim",
                get_content=True,
                save_csv=True
            )
        else:
            print(f"직접 크롤링으로 '{search_query}' 검색 중... ({display_count}개)")
            results = blog_api.search_and_get_content_without_api(
                query=search_query,
                display=display_count,
                get_content=True,
                save_csv=True
            )
        
        if results:
            all_results.extend(results)
            total_collected += len(results)
            print(f"✅ '{search_query}' 검색 완료: {len(results)}개 수집")
        else:
            print(f"❌ '{search_query}' 검색 결과 없음")
        
        # 검색어 간 간격 (마지막이 아닌 경우)
        if i < len(search_queries):
            print(f"다음 검색어 준비 중... (잠시 대기)")
            time.sleep(random.uniform(3, 6))
    
    # 최종 결과 출력
    print(f"\n{'='*60}")
    print(f"🎉 전체 검색 완료!")
    print(f"{'='*60}")
    print(f"📊 검색어 개수: {len(search_queries)}개")
    print(f"📊 총 수집된 블로그: {total_collected}개")
    print(f"📊 평균 검색어당: {total_collected/len(search_queries):.1f}개")
    
    if total_collected > 0:
        if choice == '1':
            print("📄 모든 검색 결과가 'blog_search_results.csv' 파일에 저장되었습니다.")
        else:
            print("📄 모든 검색 결과가 'blog_search_results_no_api.csv' 파일에 저장되었습니다.")
        
        print("\n검색어별 수집 결과:")
        query_counts = {}
        for result in all_results:
            # CSV에서 검색어 정보를 가져오거나, 결과에서 추출
            # 여기서는 간단히 전체 결과만 표시
            pass
        
        for i, query in enumerate(search_queries, 1):
            print(f"{i}. '{query}': 수집 완료")
    else:
        print("❌ 전체 검색에서 결과를 찾을 수 없습니다.")

if __name__ == "__main__":
    main() 