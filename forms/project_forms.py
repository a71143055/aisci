from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ChatForm(FlaskForm):
    message = TextAreaField("메시지", validators=[DataRequired(), Length(min=2, max=2000)])
    submit = SubmitField("보내기")

class SimulationForm(FlaskForm):
    idea = TextAreaField("아이디어", validators=[DataRequired(), Length(min=2, max=4000)])
    goals = TextAreaField("목표", validators=[DataRequired(), Length(min=2, max=4000)])
    constraints = TextAreaField("제약", validators=[Length(max=4000)])
    tech_stack = StringField("기술 스택(선택)", default="Flask, SQLite, JS")
    submit = SubmitField("시뮬레이션 실행")
