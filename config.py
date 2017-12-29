import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''定义程序的配置，基类包含通用配置'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1234'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MYTODOIST_MAIL_PREFIX = '[Mytodoist]'
    MYTODOIST_MAIL_SENDER = 'Mytodoist Admin <540918220@qq.com>'
    MYTODOIST_ADMIN = os.environ.get('MYTODOIST_ADMIN') or '540918220@qq.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    '''开发模式配置'''
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost:3306/mytodoist'


class TestingConfig(Config):
    TESTING = True

config = {
    'default': DevelopmentConfig
}
