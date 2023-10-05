import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DEVELOPMENT = os.environ['DEVELOPMENT']
    DEBUG = os.environ['DEBUG']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

    SQLALCHEMY_USER = os.environ['POSTGRES_USER']
    SQLALCHEMY_PASSWORD = os.environ['POSTGRES_PASSWORD']
    SQLALCHEMY_HOST = os.environ['POSTGRES_HOST']
    SQLALCHEMY_PORT = os.environ['POSTGRES_PORT']
    SQLALCHEMY_DB = os.environ['POSTGRES_DB']
    OPENAI_API_KEY = os.environ['OPENAPI_KEY']
    postgresql_string = 'postgresql://{}:{}@{}:{}/{}'
    SQLALCHEMY_DATABASE_URI = postgresql_string.format(
        SQLALCHEMY_USER, SQLALCHEMY_PASSWORD, SQLALCHEMY_HOST,
        SQLALCHEMY_PORT, SQLALCHEMY_DB)
