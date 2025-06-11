#!/usr/bin/env python3
"""
블로그 포스팅 자동생성기 서버 실행 스크립트
"""

import sys
import os
import uvicorn

def main():
    """서버 실행 메인 함수"""
    print("🤖 블로그 포스팅 자동생성기 서버를 시작합니다...")
    print("📦 모델 로딩에 시간이 걸릴 수 있습니다. 잠시만 기다려주세요.")
    print("🌐 서버가 시작되면 http://localhost:8000 에서 접속하세요.")
    print("🔄 서버를 종료하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    try:
        # 현재 디렉토리를 makeweb으로 변경
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)
        
        # FastAPI 서버 실행
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    
    except KeyboardInterrupt:
        print("\n🛑 서버가 종료되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 