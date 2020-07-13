import os


basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLACHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BLOG_TWO_MAIL_SUBJECT_PREFIX = '[BLOG 2.0]'
    BLOG_TWO_MAIL_SENDER = 'Blog 2 Admin <blogtwo@example.com'
    BLOG_TWO_ADMIN = os.environ.get("BLOG_TWO_ADMIN") or 'test@test.com'

    @staticmethod
    def init_app(app):
        # Specific initializations can be performed.
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 8025
    MAIL_USE_TLS = True
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfg(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfg,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}