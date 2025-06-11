from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from typing import Optional
import json
import traceback
from pydantic import BaseModel

app = FastAPI(title="블로그 포스팅 자동생성기")

# 정적 파일과 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class BlogGenerator:
    def __init__(self, base_model_name: str, adapter_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading base model '{base_model_name}' on {self.device}...")

        # 계산 데이터 타입을 bfloat16으로 통일하여 안정성 확보
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

        # 기본 모델 로드
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16 # 모델 기본 타입도 명시적으로 bfloat16 사용
        )
        
        # 토크나이저를 어댑터 경로에서 로드해야 합니다.
        self.tokenizer = AutoTokenizer.from_pretrained(adapter_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            base_model.config.pad_token_id = base_model.config.eos_token_id

        print(f"Loading QLoRA adapter from '{adapter_path}'...")
        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model.eval()
        print("Model and adapter loaded successfully!")

    def generate_blog_post(self, category: str, fields: dict, details: str) -> str:
        """블로그 포스트 생성 (ipynb와 프롬프트 형식 통일)"""
        
        # 1. ipynb와 동일한 프롬프트 형식을 위한 필드 문자열 생성
        key_map = {
            'store_name': '가게이름', 'taste': '맛', 'view': '경치', 
            'price': '가격', 'atmosphere': '분위기', 'food_type': '음식종류',
            'rating': '평가', 'product_name': '제품이름', 'category': '종류',
            'purpose': '용도'
        }
        
        field_parts = []
        # 'undefined' 문자열을 걸러내기 위한 조건 추가
        for key, value in fields.items():
            # 값이 존재하고, 'undefined' 문자열이 아닐 때만 추가
            if value and str(value).strip().lower() != 'undefined':
                kor_key = key_map.get(key, key)
                field_parts.append(f"[{kor_key}:{value}]")

        # 상세내용은 값이 있고, 'undefined'가 아닐 때만 (공백만 있는 경우 제외) 프롬프트에 추가
        if details and details.strip() and details.strip().lower() != 'undefined':
            field_parts.append(f"[상세내용:{details}]")
        
        field_str = "".join(field_parts)

        # 2. 카테고리별 주제 문장 설정
        subject_map = {
            "카페": "카페에 대한 글을 쓸 예정입니다.",
            "맛집": "맛집에 대한 글을 쓸 예정입니다.",
            "리뷰": "제품 리뷰에 대한 글을 쓸 예정입니다."
        }
        subject = subject_map.get(category, f"{category}에 대한 글을 쓸 예정입니다.")
        
        # 3. 최종 프롬프트 조합 (ipynb와 완전 동일)
        prompt = (
            f"당신은 블로그를 포스팅하는 블로거입니다. {subject}"
            f"{field_str} 의 내용으로 블로그를 포스팅해주세요. "
            "이모지(👍💕..)나 특수기호($*#@)는 사용하지 마세요. "
            "최대한 길게 쓰세요. 최대한 사람처럼 쓰세요."
        )

        # 디버깅을 위해 생성된 프롬프트 출력
        print("\n" + "="*50)
        print("Generated Prompt for Model:")
        print(prompt)
        print("="*50 + "\n")

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1000,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id # pad_token을 eos_token으로 설정
            )
        
        # 입력 프롬프트를 제외한 생성된 텍스트만 디코딩
        generated_text = self.tokenizer.decode(
            outputs[0],  # 전체 출력을 디코딩
            skip_special_tokens=True
        )
        
        # 프롬프트 부분을 결과에서 제거
        return generated_text[len(prompt):].strip()

# 전역 모델 인스턴스
blog_generator = None

@app.on_event("startup")
async def startup_event():
    global blog_generator
    base_model_name = "google/gemma-3-4b-it"
    # makeweb/main.py 기준 상대 경로 수정
    adapter_path = "../gemma3-4b-blog-qlora" 
    blog_generator = BlogGenerator(base_model_name=base_model_name, adapter_path=adapter_path)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """메인 페이지"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_blog(
    request: Request,
    category: str = Form(...),
    details: str = Form(...),
    cafe_taste: Optional[str] = Form(None), cafe_view: Optional[str] = Form(None), cafe_price: Optional[str] = Form(None), cafe_atmosphere: Optional[str] = Form(None), cafe_store_name: Optional[str] = Form(None),
    restaurant_taste: Optional[str] = Form(None), restaurant_food_type: Optional[str] = Form(None), restaurant_rating: Optional[str] = Form(None), restaurant_price: Optional[str] = Form(None), restaurant_store_name: Optional[str] = Form(None),
    review_category: Optional[str] = Form(None), review_rating: Optional[str] = Form(None), review_price: Optional[str] = Form(None), review_purpose: Optional[str] = Form(None), review_product_name: Optional[str] = Form(None)
):
    fields = {}
    if category == "카페":
        fields = {"taste": cafe_taste, "view": cafe_view, "price": cafe_price, "atmosphere": cafe_atmosphere, "store_name": cafe_store_name}
    elif category == "맛집":
        fields = {"taste": restaurant_taste, "food_type": restaurant_food_type, "rating": restaurant_rating, "price": restaurant_price, "store_name": restaurant_store_name}
    else:
        fields = {"category": review_category, "rating": review_rating, "price": review_price, "purpose": review_purpose, "product_name": review_product_name}
    
    try:
        generated_post = blog_generator.generate_blog_post(category, fields, details)
        return {"success": True, "generated_post": generated_post, "category": category, "fields": fields, "details": details}
    except Exception as e:
        traceback.print_exc()
        return {"success": False, "error": str(e)}

class AutocompleteRequest(BaseModel):
    prompt: str

@app.post("/text_autocomplete")
async def text_autocomplete(req: AutocompleteRequest):
    """실시간 텍스트 자동완성을 처리합니다."""
    try:
        prompt = req.prompt
        inputs = blog_generator.tokenizer(prompt, return_tensors="pt").to(blog_generator.device)

        with torch.no_grad():
            outputs = blog_generator.model.generate(
                **inputs,
                max_new_tokens=20,  # 짧고 빠른 추천을 위해
                do_sample=False,
                temperature=0.0,
                repetition_penalty=1.05,
                pad_token_id=blog_generator.tokenizer.eos_token_id
            )
        
        full_text = blog_generator.tokenizer.decode(outputs[0], skip_special_tokens=True)
        completion = full_text[len(prompt):]
        # 줄바꿈 이전의 첫번째 라인만 반환
        suggestion = completion.split("\n")[0].strip()

        return {"success": True, "suggestion": suggestion}
    except Exception as e:
        # traceback.print_exc() # 상세 오류 로깅이 필요할 때 주석 해제
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 