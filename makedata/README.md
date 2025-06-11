# 네이버 검색 API Python 클라이언트

네이버 검색 API를 사용하여 다양한 검색 서비스를 이용할 수 있는 Python 클라이언트입니다.

## 기능

- 블로그 검색
- 뉴스 검색
- 책 검색
- 백과사전 검색
- 영화 검색
- 카페글 검색
- 지식iN 검색
- 지역 검색
- 이미지 검색

## 설치

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 네이버 개발자센터 설정

1. [네이버 개발자센터](https://developers.naver.com/main/)에 접속
2. 로그인 후 "Application" → "애플리케이션 등록" 클릭
3. 애플리케이션 정보 입력:
   - 애플리케이션 이름: 원하는 이름 입력
   - 사용 API: 검색 API 선택
   - 환경: PC 웹 선택
   - 서비스 URL: http://localhost (테스트용)
4. 등록 완료 후 Client ID와 Client Secret 확인

## 사용법

### 1. API 키 설정

`naver_search.py` 파일에서 다음 부분을 수정하세요:

```python
CLIENT_ID = "YOUR_CLIENT_ID"        # 발급받은 Client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # 발급받은 Client Secret
```

### 2. 프로그램 실행

```bash
python naver_search.py
```

### 3. 사용 예제

```python
from naver_search import NaverSearchAPI

# API 인스턴스 생성
naver_api = NaverSearchAPI("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")

# 블로그 검색
blog_results = naver_api.search_blog("파이썬", display=5)

# 뉴스 검색
news_results = naver_api.search_news("인공지능", display=10, sort="date")

# 책 검색
book_results = naver_api.search_book("프로그래밍")

# 지역 검색
local_results = naver_api.search_local("강남역 맛집")
```

## API 메서드

### search_blog(query, display=10, start=1, sort="sim")
- **query**: 검색어
- **display**: 검색 결과 출력 건수 (1~100)
- **start**: 검색 시작 위치 (1~1000)
- **sort**: 정렬 옵션 ("sim": 정확도순, "date": 날짜순)

### search_news(query, display=10, start=1, sort="sim")
- 뉴스 검색 (매개변수는 블로그 검색과 동일)

### search_book(query, display=10, start=1, sort="sim")
- 책 검색 (매개변수는 블로그 검색과 동일)

### search_encyc(query, display=10, start=1)
- 백과사전 검색 (정렬 옵션 없음)

### search_movie(query, display=10, start=1)
- 영화 검색 (정렬 옵션 없음)

### search_cafearticle(query, display=10, start=1, sort="sim")
- 카페글 검색 (매개변수는 블로그 검색과 동일)

### search_kin(query, display=10, start=1, sort="sim")
- 지식iN 검색 (매개변수는 블로그 검색과 동일)

### search_local(query, display=5, start=1, sort="random")
- **query**: 검색어
- **display**: 검색 결과 출력 건수 (1~5)
- **start**: 검색 시작 위치 (1~1000)
- **sort**: 정렬 옵션 ("random": 정확도순, "comment": 업체리뷰개수순)

### search_image(query, display=10, start=1, sort="sim", filter="all")
- **query**: 검색어
- **display**: 검색 결과 출력 건수 (1~100)
- **start**: 검색 시작 위치 (1~1000)
- **sort**: 정렬 옵션 ("sim": 정확도순, "date": 날짜순)
- **filter**: 필터 옵션 ("all": 전체, "large": 큰 이미지, "medium": 중간 이미지, "small": 작은 이미지)

## 주의사항

1. 네이버 개발자센터에서 발급받은 Client ID와 Client Secret이 필요합니다.
2. API 호출 제한이 있으니 네이버 개발자센터에서 확인하세요.
3. 검색 결과에 포함된 HTML 태그는 자동으로 제거되지 않습니다.

## 라이선스

MIT License 

# 맛집 리뷰 분류기 (Gemma LLM)

이 프로젝트는 Gemma LLM을 사용하여 맛집 리뷰를 자동으로 분류하는 시스템입니다.

## 📋 분류 카테고리

리뷰는 다음 4개 카테고리로 분류됩니다:

1. **[맛]** - 맛에 대한 언급 (예: 맛있다, 달다, 짜다, 부드럽다 등)
2. **[음식종류]** - 음식의 종류나 메뉴 (예: 닭갈비, 파스타, 삼겹살, 해산물 등)
3. **[평가]** - 전반적인 평가나 만족도 (예: 좋음, 추천함, 별로임, 최고 등)
4. **[가격]** - 가격에 대한 언급 (예: 가성비좋음, 비싸다, 저렴함, 합리적 등)

## 🛠️ 설치 및 설정

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Ollama 설치

Gemma 모델을 사용하기 위해 Ollama를 설치해야 합니다.

**Windows:**
1. [Ollama 공식 웹사이트](https://ollama.ai/)에서 Windows용 설치 파일 다운로드
2. 설치 파일 실행하여 설치 완료

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Gemma 모델 다운로드

```bash
ollama pull gemma:2b
```

더 큰 모델을 원한다면:
```bash
ollama pull gemma:7b
```

## 🚀 사용법

### 기본 실행

```bash
python restaurant_classifier.py
```

### CSV 파일 형식

입력 CSV 파일은 다음 컬럼을 포함해야 합니다:
- `본문내용`: 분석할 리뷰 텍스트

### 출력 결과

분류 결과는 다음 컬럼들이 추가된 새로운 CSV 파일로 저장됩니다:
- `분류_맛`: 맛 관련 키워드
- `분류_음식종류`: 음식 종류
- `분류_평가`: 전반적 평가
- `분류_가격`: 가격 관련 정보

### 예시 결과

```
원본 리뷰: "닭갈비가 정말 맛있었어요. 가격도 저렴하고 전체적으로 만족스러웠습니다."

분류 결과:
- 맛: 맛있었어요
- 음식종류: 닭갈비
- 평가: 만족스러웠습니다
- 가격: 저렴하고
```

## ⚙️ 설정 옵션

### 모델 변경

`restaurant_classifier.py` 파일에서 모델을 변경할 수 있습니다:

```python
# 더 빠른 모델 (2B 파라미터)
classifier = RestaurantReviewClassifier(model_name="gemma:2b")

# 더 정확한 모델 (7B 파라미터)
classifier = RestaurantReviewClassifier(model_name="gemma:7b")
```

### 처리할 샘플 수 조정

```python
# 전체 데이터 처리
classifier.classify_csv_file(input_file, output_file, sample_size=None)

# 처음 100개만 처리
classifier.classify_csv_file(input_file, output_file, sample_size=100)
```

## 📁 파일 구조

```
├── blog_search_results.csv          # 입력 CSV 파일
├── restaurant_classifier.py         # 메인 분류 스크립트
├── classified_restaurant_reviews.csv # 출력 결과 파일
├── requirements.txt                 # Python 패키지 목록
└── README.md                       # 이 파일
```

## 🔧 문제 해결

### Ollama 연결 오류
```
모델 확인 중 오류 발생: ...
```
- Ollama 서비스가 실행 중인지 확인하세요
- Windows: 작업 관리자에서 Ollama 프로세스 확인
- macOS/Linux: `ollama serve` 명령으로 수동 실행

### 메모리 부족 오류
- 더 작은 모델 사용: `gemma:2b` 대신 사용
- 처리할 샘플 수 줄이기: `sample_size` 파라미터 조정

### CSV 인코딩 오류
- 입력 파일이 UTF-8 인코딩인지 확인
- Excel에서 저장할 때 "CSV UTF-8" 형식 선택

## 📊 성능 참고사항

- **gemma:2b**: 빠른 처리, 기본적인 정확도
- **gemma:7b**: 느린 처리, 높은 정확도
- 평균 처리 속도: 리뷰당 1-3초 (모델과 하드웨어에 따라 차이)

## 🤝 기여하기

버그 리포트나 기능 제안은 이슈로 등록해주세요!

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 