import pytest
from app import create_app
from app.database import db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'test'
    MYSQL_PASSWORD = 'test'
    MYSQL_DB = 'test_db'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()