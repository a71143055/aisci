import os
from textwrap import dedent

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_project_files(base_dir: str, report: dict):
    # README
    write_file(
        os.path.join(base_dir, "README.md"),
        dedent(f"""
        # Generated Project (aisci)

        **아이디어:** {report['idea']}
        **목표:** {report['goals']}
        **제약:** {report['constraints']}
        **기술스택:** {report['tech_stack']}

        ## LLM 설계 요약
        {report['llm_design_summary']}

        ## 구조
        - src/: 핵심 코드
        - tests/: 간단 테스트
        - docs/: 분석/설계 문서
        - configs/: 설정
        - logs/: 실행 로그
        """).strip()
    )

    # src/main.py
    write_file(
        os.path.join(base_dir, "src", "main.py"),
        dedent("""
        import json

        def run():
            print("시뮬레이션 러너 실행")
            data = {"status": "ok", "message": "프로젝트 스캐폴딩 완료"}
            print(json.dumps(data, ensure_ascii=False))

        if __name__ == "__main__":
            run()
        """).strip()
    )

    # src/analyze.py
    write_file(
        os.path.join(base_dir, "src", "analyze.py"),
        dedent("""
        def summarize_requirements(idea, goals, constraints):
            summary = [
                f"아이디어: {idea[:80]}",
                f"목표: {goals[:80]}",
                f"제약: {constraints[:80]}",
                "권장: 로깅/테스트/설정 분리"
            ]
            return "\\n".join(summary)
        """).strip()
    )

    # tests/test_basic.py
    write_file(
        os.path.join(base_dir, "tests", "test_basic.py"),
        dedent("""
        def test_basic():
            assert 1 + 1 == 2
        """).strip()
    )

    # docs/analysis.md
    write_file(
        os.path.join(base_dir, "docs", "analysis.md"),
        dedent(f"""
        # 분석 리포트

        - 아이디어: {report['idea']}
        - 목표: {report['goals']}
        - 제약: {report['constraints']}

        ## 제안 아키텍처
        {report['llm_design_summary']}
        """).strip()
    )

    # configs/default.yaml
    write_file(
        os.path.join(base_dir, "configs", "default.yaml"),
        dedent("""
        app:
          name: generated-app
          env: dev
        logging:
          level: INFO
        """).strip()
    )

    # logs/app.log
    write_file(
        os.path.join(base_dir, "logs", "app.log"),
        "초기 로그\n"
    )
