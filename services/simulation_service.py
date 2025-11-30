import os
import datetime
from typing import Tuple, Dict
from utils.project_templates import generate_project_files

class SimulationService:
    """
    사람의 생각(아이디어/목표/제약/기술스택)을 받아
    - 설계 요약(LLM)
    - 파일/디렉터리 자동 생성
    - 분석 리포트 생성
    """
    def __init__(self, llm, base_output_dir: str):
        self.llm = llm
        self.base_output_dir = base_output_dir

    def run(self, user, idea: str, goals: str, constraints: str, tech_stack: str) -> Tuple[str, Dict]:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"aisci_{getattr(user, 'id', 'anon')}_{ts}"
        project_dir = os.path.join(self.base_output_dir, safe_name)
        os.makedirs(project_dir, exist_ok=True)

        # LLM로 설계 요약 요청
        prompt = (
            f"아이디어: {idea}\n목표: {goals}\n제약: {constraints}\n기술스택: {tech_stack}\n\n"
            "위 내용을 바탕으로 구현 가능한 모듈/컴포넌트로 분해하고, 디렉터리/파일 구조와 주요 코드 스캐폴딩을 제안하라."
        )
        design_summary = self.llm.generate_response(prompt=prompt, system_prompt="프로젝트 설계 보조자 역할을 수행하라.")

        report = {
            "idea": idea,
            "goals": goals,
            "constraints": constraints,
            "tech_stack": tech_stack,
            "llm_design_summary": design_summary
        }

        # 파일 생성
        generate_project_files(project_dir, report)

        return project_dir, report
