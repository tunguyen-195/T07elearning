# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    fullname = StringField('Họ và Tên', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Đăng ký')


# class RegisterForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     phone = StringField('Phone Number', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Register')


class ResetPasswordForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Khôi phục mật khẩu')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')
