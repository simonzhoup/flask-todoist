from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp


class UserRegister(FlaskForm):
    username = StringField('用户名：', validators=[Required(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9]*$', 0, 'Usernames must have only letters,numbers,')])
    password = PasswordField('密码：', validators=[Required()])
    submit = SubmitField('提交')


class UserLogin(FlaskForm):
    username = StringField('用户名：', validators=[Required(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9]*$', 0, 'Usernames must have only letters,numbers,')])
    password = PasswordField('密码：', validators=[Required()])
    remeber_me = BooleanField('记住我')
    submit = SubmitField('登录')
