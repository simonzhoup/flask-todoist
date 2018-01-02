from . import db
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    '''flask-login 必需的回调函数，从数据库中通过id找到用户'''
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64), index=True)
    icon = db.Column(db.String(64), default='file')
    tasks = db.relationship('Task', backref='project_task')

    def default_project(user):
        projects = [['个人', 'user'], ['工作', 'paperclip'], [
            '购物', 'shopping-cart'], ['饮食', 'cutlery'], ['杂项', 'certificate']]
        for p in projects:
            project = Project(name=p[0], user_id=user.id, icon=p[1])
            db.session.add(project)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    timenode = db.Column(db.Date, index=True)
    priority = db.Column(db.Integer, index=True, default=1)
    project = db.Column(db.String(64), db.ForeignKey('projects.name'))
