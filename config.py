import os
basedir = os.path.abspath(os.path.dirname(__file__))
#PASSWORD = os.getenv("PASSWORD")

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'  # os.environ.get('MYSQLUSER')
PASSWORD = 'cgh1998922'  # os.environ.get('MYSQLPASSWORD')
HOST = '127.0.0.1'  # os.environ.get('MYSQLHOST')
PORT = '3306'
DATABASE = 'feed'

class Config:
    SECRET_KEY = 'CCNU MUXI BEST TEAM'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <1113713599@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@localhost/{}?charset=utf8".format(
            DIALECT, DRIVER, USERNAME, PASSWORD, DATABASE)
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@localhost/{}?charset=utf8".format(
            DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        "{}+{}://{}:{}@localhost/{}?charset=utf8".format(
            DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

config = {
    'developments': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
