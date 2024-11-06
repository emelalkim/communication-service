import pytest
from app import create_app
from app.database import db

@pytest.fixture
def app():
    # Create the app instance using the factory function
    app = create_app()

    # Set up the application context and initialize the database
    with app.app_context():
        db.create_all()  # Create tables in the in-memory database
    
    yield app

    # Teardown: Drop all tables after the test is complete
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    # Use the test client for making requests to the app
    return app.test_client()
