# aisci

Flask 기반의 AI Scientist 시뮬레이터(프로젝트 스캐폴딩 + ZIP 출력).

## 요구사항
- Python 3.10+
- 권장: Conda 환경

## 설치
```bash
conda create -n aisci python=3.10 -y
conda activate aisci
pip install -r requirements.txt

SECRET_KEY=your_secret
LLM_PROVIDER=mock  # or ollama
OLLAMA_MODEL=llama3.1
OLLAMA_URL=http://localhost:11434/api/generate
DATABASE_URL=sqlite:///aisci.db

python --version

python app.py
# 또는 run.bat 실행 (Windows)
# 접속: http://127.0.0.1:5000

---

### 마무리 메모
- 위 코드는 **개발·프로토타입 목적**으로 구성되어 있습니다. 운영 환경에서는 세션 관리, CSRF, 입력 검증, LLM 호출 제한, 로깅, 에러 모니터링, 마이그레이션(Flask-Migrate) 등을 추가로 구성하세요.  
- 원하시면 **(1)** Ollama 응답 구조에 맞춘 파싱 테스트 코드, **(2)** PyCharm 실행 구성 파일, **(3)** 도메인별 템플릿(생명과학/로보틱스 등) 중 하나를 바로 생성해 드리겠습니다.