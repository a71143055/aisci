import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from config import Config
from extensions import db, login_manager, migrate, csrf
from models.user import User
from forms.auth_forms import LoginForm, RegisterForm
from forms.project_forms import ChatForm, SimulationForm
from services.llm_service import LLMService
from services.simulation_service import SimulationService
from utils.zip_utils import zip_project

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.login_view = "login"
    login_manager.login_message = "로그인이 필요합니다."

    # 블루프린트가 없으므로 라우트 직접 정의
    @app.before_first_request
    def ensure_dirs():
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        with app.app_context():
            db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            if db.session.query(User).filter_by(email=email).first():
                flash("이미 등록된 이메일입니다.", "warning")
                return redirect(url_for("register"))
            user = User(email=email, name=form.name.data.strip())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("회원가입 완료. 로그인 해주세요.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            user = db.session.query(User).filter_by(email=email).first()
            if not user or not user.check_password(form.password.data):
                flash("이메일 또는 비밀번호가 올바르지 않습니다.", "danger")
                return redirect(url_for("login"))
            from flask_login import login_user
            login_user(user)
            flash("로그인 성공", "success")
            return redirect(url_for("chat"))
        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout():
        from flask_login import logout_user
        logout_user()
        flash("로그아웃 되었습니다.", "info")
        return redirect(url_for("index"))

    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        from flask_login import current_user, login_required
        if not getattr(current_user, "is_authenticated", False):
            return redirect(url_for("login"))
        form = ChatForm()
        messages = []
        if form.validate_on_submit():
            user_input = form.message.data
            llm = LLMService(provider=app.config["LLM_PROVIDER"], model=app.config["OLLAMA_MODEL"], url=app.config["OLLAMA_URL"])
            reply = llm.generate_response(user_input, system_prompt=(
                "너는 프로젝트 설계 보조 과학자다. 사용자의 목표를 명확화하고 구현 가능한 태스크로 분해하라."
            ))
            messages.append(("user", user_input))
            messages.append(("assistant", reply))
            flash("응답 생성 완료", "success")
        return render_template("chat.html", form=form, messages=messages)

    @app.route("/simulate", methods=["GET", "POST"])
    def simulate():
        from flask_login import current_user
        if not getattr(current_user, "is_authenticated", False):
            return redirect(url_for("login"))
        form = SimulationForm()
        result = None
        if form.validate_on_submit():
            idea = form.idea.data
            goals = form.goals.data
            constraints = form.constraints.data
            tech_stack = form.tech_stack.data or "Flask, SQLite, JS"
            llm = LLMService(provider=app.config["LLM_PROVIDER"], model=app.config["OLLAMA_MODEL"], url=app.config["OLLAMA_URL"])
            simulator = SimulationService(llm=llm, base_output_dir=app.config["UPLOAD_FOLDER"])
            project_dir, summary = simulator.run(
                user=current_user,
                idea=idea,
                goals=goals,
                constraints=constraints,
                tech_stack=tech_stack
            )
            zip_path = zip_project(project_dir)
            result = {
                "summary": summary,
                "project_dir": project_dir,
                "zip_path": zip_path
            }
            flash("프로젝트 생성 완료", "success")
        return render_template("simulate.html", form=form, result=result)

    @app.route("/download")
    def download():
        from flask_login import current_user
        if not getattr(current_user, "is_authenticated", False):
            return redirect(url_for("login"))
        zip_path = request.args.get("path")
        if not zip_path or not os.path.exists(zip_path):
            flash("다운로드할 파일이 없습니다.", "warning")
            return redirect(url_for("simulate"))
        return send_file(zip_path, as_attachment=True)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
