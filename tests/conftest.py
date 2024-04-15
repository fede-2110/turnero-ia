# conftest.py
import pytest
from flask import Flask
from src.model.db import db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use SQLite for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SERVER_NAME'] = 'localhost:5000'
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    """Creates a new database session for a test within an application context, with data cleanup."""
    with app.app_context():
        db.session.begin_nested()  # Start a transaction or savepoint
        yield db.session
        db.session.rollback()  # Roll back to savepoint or transaction start
        db.drop_all()          # Eliminar todas las tablas
        db.create_all()        # Recrear las tablas

