import os
import requests
from typing import Optional

class LLMService:
    """
    LLM 추상화 레이어.
    provider: "mock" 또는 "ollama"
    url: Ollama 엔드포인트 (환경변수로 전달)
    """
    def __init__(self, provider: str = "mock", model: str = "llama3.1", url: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.url = url or os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")

    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        if self.provider != "ollama":
            return self._mock_response(prompt, system_prompt)
        return self._ollama_response(prompt, system_prompt)

    def _mock_response(self, prompt: str, system_prompt: str) -> str:
        return (
            "요약된 목표/태스크:\n"
            f"- 시스템프롬프트: {system_prompt[:60]}...\n"
            f"- 사용자요청: {prompt}\n"
            "- 태스크 분해: 요구사항 정리 → 데이터/리소스 파악 → 아키텍처 설계 → 코드 스캐폴딩 → 테스트/배포 준비\n"
            "- 다음 단계: 시뮬레이션 페이지에서 아이디어/목표/제약을 입력하세요."
        )

    def _ollama_response(self, prompt: str, system_prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUser: {prompt}",
            "stream": False
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            # Ollama 응답 구조에 따라 조정 필요
            if isinstance(data, dict):
                # 흔한 필드들 중 하나를 반환
                return data.get("response") or data.get("text") or data.get("output") or str(data)
            return str(data)
        except requests.Timeout:
            return "오류: LLM 요청이 타임아웃되었습니다."
        except requests.RequestException as e:
            return f"오류: LLM 호출 실패 ({e})"
