#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
맛집 리뷰 분류기 테스트 스크립트

이 스크립트는 몇 개의 샘플 리뷰로 분류기를 테스트합니다.
"""

import pandas as pd
from restaurant_classifier import RestaurantReviewClassifier
import json

def test_single_reviews():
    """개별 리뷰 테스트"""
    print("=== 개별 리뷰 분류 테스트 ===\n")
    
    # 분류기 초기화
    classifier = RestaurantReviewClassifier(model_name="gemma:2b")
    
    # 모델 확인
    if not classifier.pull_model_if_needed():
        print("❌ Gemma 모델을 사용할 수 없습니다.")
        print("Ollama가 설치되어 있는지 확인해주세요.")
        return False
    
    # 테스트 리뷰들
    test_reviews = [
        "닭갈비가 정말 맛있었어요! 가격도 저렴하고 전체적으로 만족스러웠습니다.",
        "파스타가 너무 짜서 별로였어요. 가격대비 품질이 아쉽습니다.",
        "삼겹살이 부드럽고 맛있네요. 가성비 최고에요! 완전 추천합니다.",
        "피자가 달콤하고 맛있어요. 하지만 좀 비싼 편이에요.",
        "해산물 요리가 신선하고 좋았습니다. 분위기도 좋고 재방문 의사 있어요."
    ]
    
    # 각 리뷰 분류
    for i, review in enumerate(test_reviews, 1):
        print(f"📝 테스트 {i}:")
        print(f"리뷰: {review}")
        
        try:
            result = classifier.classify_single_review(review)
            
            print("분류 결과:")
            print(f"  맛: {result.get('맛', '정보없음')}")
            print(f"  음식종류: {result.get('음식종류', '정보없음')}")
            print(f"  평가: {result.get('평가', '정보없음')}")
            print(f"  가격: {result.get('가격', '정보없음')}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            print("-" * 60)
    
    return True

def create_sample_csv():
    """테스트용 샘플 CSV 파일 생성"""
    print("\n=== 샘플 CSV 파일 생성 ===")
    
    sample_data = {
        '검색어': ['맛집'] * 5,
        '본문내용': [
            "닭갈비가 정말 맛있었어요! 가격도 저렴하고 전체적으로 만족스러웠습니다. 양도 충분하고 직원분들도 친절해요.",
            "파스타가 너무 짜서 별로였어요. 가격대비 품질이 아쉽습니다. 다시 가고 싶지 않네요.",
            "삼겹살이 부드럽고 맛있네요. 가성비 최고에요! 완전 추천합니다. 사장님도 정말 친절하세요.",
            "피자가 달콤하고 맛있어요. 치즈도 쫄깃하고 도우도 바삭해요. 하지만 좀 비싼 편이에요.",
            "해산물 요리가 신선하고 좋았습니다. 회가 정말 달콤하고 맛있어요. 분위기도 좋고 재방문 의사 있어요."
        ],
        '제목': [
            "맛있는 닭갈비 맛집 후기",
            "파스타 맛집이라고 해서 갔는데...",
            "삼겹살 진짜 맛집 발견!",
            "피자 맛집 추천",
            "해산물 요리 전문점 후기"
        ],
        '블로거': ['테스트블로거'] * 5,
        '작성일': ['2024-01-01'] * 5,
        '링크': ['http://test.com'] * 5
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_reviews.csv', index=False, encoding='utf-8-sig')
    print("✅ 'sample_reviews.csv' 파일이 생성되었습니다.")
    
    return 'sample_reviews.csv'

def test_csv_classification():
    """CSV 파일 분류 테스트"""
    print("\n=== CSV 파일 분류 테스트 ===")
    
    # 샘플 CSV 생성
    sample_file = create_sample_csv()
    
    # 분류기 초기화
    classifier = RestaurantReviewClassifier(model_name="gemma:2b")
    
    try:
        # CSV 파일 분류
        output_file = 'test_classified_reviews.csv'
        classifier.classify_csv_file(
            input_file=sample_file,
            output_file=output_file,
            sample_size=None  # 전체 처리 (샘플이 적으므로)
        )
        
        # 결과 출력
        classifier.show_sample_results(output_file, num_samples=5)
        
        print(f"\n✅ 분류 결과가 '{output_file}'에 저장되었습니다.")
        
    except Exception as e:
        print(f"❌ CSV 분류 중 오류 발생: {e}")

def main():
    """메인 테스트 함수"""
    print("🧪 맛집 리뷰 분류기 테스트 시작\n")
    
    # 개별 리뷰 테스트
    if test_single_reviews():
        # CSV 파일 테스트
        test_csv_classification()
    
    print("\n🎉 테스트 완료!")
    print("\n💡 팁:")
    print("- 실제 데이터 처리는 'python restaurant_classifier.py' 실행")
    print("- 모델 변경은 스크립트 내 model_name 파라미터 수정")
    print("- 처리 속도가 느리면 gemma:2b 모델 사용 권장")

if __name__ == "__main__":
    main() 