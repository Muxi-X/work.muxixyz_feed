import os
basedir = os.path.abspath(os.path.dirname(__file__))
#PASSWORD = os.getenv("PASSWORD")

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = os.getenv("WORKBENCH_USERNAME")
PASSWORD = os.getenv("WORKBENCH_PASSWORD")
HOST = os.getenv("WORKBENCH_HOST")
PORT = 3306
DATABASE = os.getenv("WORKBENCH_DBNAME")
SERCET_WORK_KEY = os.getenv("WORKBENCH_SECRET_WORK_KEY")


class Config:
    SECRET_KEY = SECRET_WORK_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <>'
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
