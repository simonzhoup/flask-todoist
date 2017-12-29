from flask import render_template, redirect, url_for, abort
from . import user
from .forms import UserRegister, UserLogin
from ..models import User
from .. import db


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegister()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        print(form.username.data)
        db.session.add(user)
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            pass
        else:
            abort(404)
        return redirect(url_for('main.index'))
    return render_template('user/login.html', form=form)
