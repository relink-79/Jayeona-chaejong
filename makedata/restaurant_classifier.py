import pandas as pd
import ollama
import json
import re
from typing import Dict, List, Tuple
import time

class RestaurantReviewClassifier:
    def __init__(self, model_name: str = "gemma:2b"):
        """
        맛집 리뷰 분류기 초기화
        
        Args:
            model_name: 사용할 Gemma 모델명 (예: "gemma:2b", "gemma:7b")
        """
        self.model_name = model_name
        self.client = ollama.Client()
        
        # 분류 프롬프트 템플릿
        self.classification_prompt = """
다음 맛집 리뷰를 분석하여 아래 4개 카테고리로 분류해주세요:

1. [맛] - 맛에 대한 언급 (예: 맛있다, 달다, 짜다, 부드럽다 등)
2. [음식종류] - 음식의 종류나 메뉴 (예: 닭갈비, 파스타, 삼겹살, 해산물 등)
3. [평가] - 전반적인 평가나 만족도 (예: 좋음, 추천함, 별로임, 최고 등)
4. [가격] - 가격에 대한 언급 (예: 가성비좋음, 비싸다, 저렴함, 합리적 등)

리뷰 내용: {review_text}

결과를 다음 JSON 형식으로 답변해주세요:
{{
    "맛": "추출된 맛 관련 키워드",
    "음식종류": "추출된 음식 종류",
    "평가": "추출된 평가 내용",
    "가격": "추출된 가격 관련 내용"
}}

만약 해당 카테고리에 대한 정보가 없으면 "정보없음"으로 표시해주세요.
"""

    def check_model_availability(self) -> bool:
        """Gemma 모델이 사용 가능한지 확인"""
        try:
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]
            return self.model_name in available_models
        except Exception as e:
            print(f"모델 확인 중 오류 발생: {e}")
            return False

    def pull_model_if_needed(self) -> bool:
        """필요시 Gemma 모델 다운로드"""
        if not self.check_model_availability():
            print(f"{self.model_name} 모델을 다운로드 중입니다...")
            try:
                self.client.pull(self.model_name)
                print("모델 다운로드 완료!")
                return True
            except Exception as e:
                print(f"모델 다운로드 실패: {e}")
                return False
        return True

    def classify_single_review(self, review_text: str) -> Dict[str, str]:
        """
        단일 리뷰를 분류
        
        Args:
            review_text: 분류할 리뷰 텍스트
            
        Returns:
            분류 결과 딕셔너리
        """
        try:
            # 프롬프트 생성
            prompt = self.classification_prompt.format(review_text=review_text[:1000])  # 텍스트 길이 제한
            
            # Gemma 모델에 요청
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            # 응답에서 JSON 추출
            response_text = response['message']['content']
            
            # JSON 부분만 추출
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                try:
                    result = json.loads(json_str)
                    return result
                except json.JSONDecodeError:
                    print(f"JSON 파싱 오류: {json_str}")
                    return self._create_empty_result()
            else:
                print(f"JSON 형식을 찾을 수 없음: {response_text}")
                return self._create_empty_result()
                
        except Exception as e:
            print(f"분류 중 오류 발생: {e}")
            return self._create_empty_result()

    def _create_empty_result(self) -> Dict[str, str]:
        """빈 결과 생성"""
        return {
            "맛": "정보없음",
            "음식종류": "정보없음", 
            "평가": "정보없음",
            "가격": "정보없음"
        }

    def classify_csv_file(self, input_file: str, output_file: str, sample_size: int = None) -> None:
        """
        CSV 파일의 리뷰들을 분류
        
        Args:
            input_file: 입력 CSV 파일 경로
            output_file: 출력 CSV 파일 경로
            sample_size: 처리할 샘플 수 (None이면 전체)
        """
        print("CSV 파일을 읽는 중...")
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # 샘플 크기 설정
        if sample_size:
            df = df.head(sample_size)
            print(f"샘플 {sample_size}개로 제한하여 처리합니다.")
        
        print(f"총 {len(df)}개의 리뷰를 처리합니다.")
        
        # 결과 저장을 위한 새로운 컬럼들
        df['분류_맛'] = ''
        df['분류_음식종류'] = ''
        df['분류_평가'] = ''
        df['분류_가격'] = ''
        
        # 각 리뷰 분류
        for idx, row in df.iterrows():
            print(f"처리 중: {idx + 1}/{len(df)}")
            
            review_text = str(row['본문내용'])
            if pd.isna(review_text) or review_text.strip() == '':
                continue
                
            # 분류 수행
            result = self.classify_single_review(review_text)
            
            # 결과 저장
            df.at[idx, '분류_맛'] = result.get('맛', '정보없음')
            df.at[idx, '분류_음식종류'] = result.get('음식종류', '정보없음')
            df.at[idx, '분류_평가'] = result.get('평가', '정보없음')
            df.at[idx, '분류_가격'] = result.get('가격', '정보없음')
            
            # 너무 빠르게 요청하지 않도록 잠시 대기
            time.sleep(1)
        
        # 결과 저장
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"분류 결과가 '{output_file}'에 저장되었습니다.")

    def show_sample_results(self, output_file: str, num_samples: int = 5) -> None:
        """분류 결과 샘플 출력"""
        df = pd.read_csv(output_file, encoding='utf-8-sig')
        
        print(f"\n=== 분류 결과 샘플 ({num_samples}개) ===")
        for idx in range(min(num_samples, len(df))):
            row = df.iloc[idx]
            print(f"\n#{idx + 1}")
            print(f"원본 리뷰: {row['본문내용'][:100]}...")
            print(f"맛: {row['분류_맛']}")
            print(f"음식종류: {row['분류_음식종류']}")
            print(f"평가: {row['분류_평가']}")
            print(f"가격: {row['분류_가격']}")
            print("-" * 50)


def main():
    """메인 실행 함수"""
    print("=== 맛집 리뷰 분류기 (Gemma LLM) ===\n")
    
    # 분류기 초기화
    classifier = RestaurantReviewClassifier(model_name="gemma:2b")
    
    # 모델 확인 및 다운로드
    if not classifier.pull_model_if_needed():
        print("Gemma 모델을 사용할 수 없습니다. Ollama가 설치되어 있는지 확인해주세요.")
        return
    
    # 입력/출력 파일 설정
    input_file = "blog_search_results.csv"
    output_file = "classified_restaurant_reviews.csv"
    
    # 테스트를 위해 처음 10개만 처리 (전체 처리하려면 sample_size=None 설정)
    print("테스트를 위해 처음 10개 리뷰만 처리합니다.")
    print("전체 처리를 원하시면 sample_size=None으로 변경해주세요.\n")
    
    try:
        # 분류 수행
        classifier.classify_csv_file(
            input_file=input_file,
            output_file=output_file,
            sample_size=10  # 테스트용, 전체 처리시 None
        )
        
        # 결과 샘플 출력
        classifier.show_sample_results(output_file, num_samples=5)
        
    except FileNotFoundError:
        print(f"'{input_file}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main() 