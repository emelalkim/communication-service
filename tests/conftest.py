import pytest
from app import app as flask_app
from database import db
from config import TestConfig

@pytest.fixture
def app():
    # Configure the app for testing
    flask_app.config.from_object(TestConfig)
    with flask_app.app_context():
        db.create_all()  # Create tables in the in-memory database
    yield flask_app
    with flask_app.app_context():
        db.drop_all()  # Drop tables after tests complete

@pytest.fixture
def client(app):
    return app.test_client()
