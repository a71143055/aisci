from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField("이름", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("이메일", validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("회원가입")

class LoginForm(FlaskForm):
    email = StringField("이메일", validators=[DataRequired(), Email()])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    submit = SubmitField("로그인")
