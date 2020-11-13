import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    uri = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        os.getenv('DATABASE_PASSWORD'),
        os.getenv('DATABASE_SCHEMA_NAME')
    )
    uri_without_schema = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        os.getenv('DATABASE_PASSWORD'),
    )

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_DATABASE_URI_WITHOUT_SCHEMA = uri_without_schema


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
