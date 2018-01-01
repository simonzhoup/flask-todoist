from flask import render_template, redirect, url_for, abort, flash, request, current_app
from . import user
from .forms import UserRegister, UserLogin
from ..models import User
from .. import db
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..email import send_email


@user.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'user.' and request.endpoint != 'static':
        return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegister()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(to=user.email, subject='请验证您的邮箱',
                   template='confirm', user=user, token=token)
        flash('注册成功')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('帐号/密码不正确')
        return redirect(url_for('main.index'))
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已登出')
    return redirect(url_for('main.index'))


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您的邮箱验证通过，谢谢！')
    else:
        flash('请检查链接有效，并且没有过期。')
    return redirect(url_for('main.index'))


@user.route('/confirm')
@login_required
def resend_email():
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email, subject='请验证您的邮箱',
               template='confirm', user=current_user, token=token)
    flash('一封新的账户验证邮件已发送到您的邮箱，请注意查收。')
    return redirect(url_for('main.index'))
