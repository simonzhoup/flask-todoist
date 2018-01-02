from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


class UserRegister(FlaskForm):
    username = StringField('用户名：', validators=[Required(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9]*$', 0, 'Usernames must have only letters,numbers,')])
    email = StringField('邮箱：', validators=[Required(), Email()])
    password = PasswordField(
        '密码：', validators=[Required(), EqualTo('password2', message='两次密码输入不一致')])
    password2 = PasswordField('确认密码：', validators=[Required()])
    submit = SubmitField('马上注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class UserLogin(FlaskForm):
    username = StringField('', validators=[Required(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9]*$', 0, 'Usernames must have only letters,numbers,')])
    password = PasswordField('', validators=[Required()])
    submit = SubmitField('登录')
