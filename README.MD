# emma 모델을 이용한 블로그 포스트 자동 생성기

## 프로젝트 설명

이 프로젝트는 Naver 블로그에서 리뷰 데이터를 수집하고, Gemma 모델을 fine-tuning하여 사용자가 입력한 키워드를 기반으로 자동으로 블로그 포스트를 생성하는 웹 애플리케이션입니다.

## 프로젝트 구조

```
.
├── makedata/              # Naver 블로그 데이터 수집 및 전처리
│   ├── naver_search.py
│   ├── restaurant_classifier.py
│   └── requirements.txt
├── makemodel/             # Gemma 모델 Fine-tuning (QLoRA)
│   ├── Tunning.ipynb
│   └── requirements.txt
├── makeweb/               # 블로그 생성 웹 애플리케이션 (FastAPI)
│   ├── main.py
│   ├── run_server.py
│   └── requirements.txt
├── gemma3-4b-blog-qlora/  # Fine-tuning된 모델 어댑터 저장 디렉토리
└── README.MD
```

## 주요 기술

-   **Backend:** FastAPI
-   **Frontend:** HTML, Jinja2
-   **Crawling:** Selenium, BeautifulSoup
-   **ML/DL:** PyTorch, Transformers, PEFT (QLoRA), Ollama
-   **Model:** Google Gemma
