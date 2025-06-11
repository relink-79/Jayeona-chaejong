# 🤖 블로그 포스팅 자동생성기

AI(Gemma LLM)를 활용한 스마트 블로그 포스팅 자동생성 웹 서비스입니다.

## ✨ 주요 기능

- 📝 **3가지 카테고리 지원**: 카페, 맛집, 리뷰
- 🎯 **카테고리별 맞춤 입력 필드**
  - **카페**: 맛, 경치, 가격, 분위기, 가게이름
  - **맛집**: 맛, 음식종류, 평가, 가격, 가게이름  
  - **리뷰**: 종류, 평가, 가격, 용도, 제품이름
- 🔮 **AI 자동완성** 기능
- 📋 **원클릭 복사** 기능
- 💻 **반응형 디자인** (모바일 지원)
- ⚡ **실시간 생성** (로컬 LLM 사용)

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
cd makeweb
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python run_server.py
```
또는
```bash
python main.py
```

### 3. 웹 접속
브라우저에서 `http://localhost:8000` 접속

## 📖 사용법

### 기본 사용 순서
1. **카테고리 선택**: 카페/맛집/리뷰 중 하나 선택
2. **정보 입력**: 선택한 카테고리에 맞는 정보 입력
3. **상세내용 작성**: 추가로 포함하고 싶은 내용 입력
4. **포스트 생성**: "전송" 버튼 클릭
5. **결과 확인**: 생성된 블로그 포스트 확인 및 복사

### 🎯 카테고리별 입력 필드

#### ☕ 카페
- **가게이름**: 카페 이름
- **맛**: 커피나 음료의 맛 (예: 부드럽고 달콤함)
- **경치**: 뷰나 풍경 (예: 바다가 보임, 도심 뷰)
- **분위기**: 카페 분위기 (예: 아늑함, 모던함)
- **가격**: 가격대 평가 (예: 가성비 좋음, 조금 비쌈)

#### 🍽️ 맛집
- **가게이름**: 음식점 이름
- **맛**: 음식의 맛 (예: 진하고 맛있음)
- **음식종류**: 메뉴 종류 (예: 파스타, 삼겹살)
- **평가**: 전체적인 평가 (예: 추천함, 재방문 의사)
- **가격**: 가격대 평가 (예: 가성비 좋음, 조금 비쌈)

#### ⭐ 리뷰
- **제품이름**: 리뷰할 제품명
- **종류**: 제품 카테고리 (예: 전자제품, 화장품)
- **평가**: 사용 후 평가 (예: 만족함, 추천함)
- **용도**: 사용 목적 (예: 일상용, 선물용)
- **가격**: 가격대 평가 (예: 가성비 좋음, 조금 비쌈)

### ✨ 고급 기능

#### 🔮 Autocomplete (자동완성)
- 일부 정보만 입력한 상태에서 "Autocomplete" 버튼 클릭
- AI가 누락된 정보에 대한 추천을 제공
- 생성된 추천 내용을 참고하여 빈 필드를 채움

#### ⌨️ 키보드 단축키
- `Ctrl + Enter`: 포스트 생성
- `Esc`: 결과창 닫기

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 웹 프레임워크
- **PyTorch**: 딥러닝 프레임워크
- **Transformers**: Hugging Face 모델 라이브러리
- **Gemma-2b-it**: Google의 경량화 LLM

### Frontend
- **HTML5/CSS3**: 웹 표준
- **JavaScript (ES6+)**: 동적 기능
- **Responsive Design**: 모바일 지원

## ⚙️ 시스템 요구사항

### 최소 요구사항
- **Python**: 3.8 이상
- **RAM**: 8GB 이상
- **저장공간**: 10GB 이상 (모델 포함)

### 권장 요구사항
- **GPU**: CUDA 지원 GPU (RTX 3060 이상)
- **RAM**: 16GB 이상
- **저장공간**: 20GB 이상

## 🔧 설정 옵션

### 모델 변경
`main.py`에서 모델명 변경 가능:
```python
blog_generator = BlogGenerator(model_name="google/gemma-2b-it")
```

### 서버 포트 변경
`run_server.py`에서 포트 설정 변경:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8080)  # 8080으로 변경
```

## 🐛 문제 해결

### CUDA 오류 발생 시
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 모델 로딩 실패 시
- 인터넷 연결 확인
- Hugging Face 토큰 확인
- 디스크 용량 확인

### 메모리 부족 시
- 브라우저 탭 정리
- 다른 프로그램 종료
- 더 작은 모델로 변경

## 📁 프로젝트 구조

```
makeweb/
├── main.py              # FastAPI 메인 애플리케이션
├── run_server.py        # 서버 실행 스크립트
├── requirements.txt     # Python 의존성
├── templates/           # HTML 템플릿
│   └── index.html      # 메인 페이지
└── static/             # 정적 파일
    ├── style.css       # 스타일시트
    └── script.js       # JavaScript
```

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 📞 지원

문제가 있거나 제안사항이 있으시면 이슈를 생성해주세요.

---

**�� 즐거운 블로그 작성되세요!** 