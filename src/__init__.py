import os
from flask import Flask
from src.model.db import db
from flask_restx import Api
from src.controllers import register_controllers
from src.error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    # Documentacion Swagger
    api = Api(app, version='1.0', title='Turnero API', description='Una API para gestionar turnos y citas médicas')
        
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # Registro de Controladores
    register_controllers(api)
    
    # Global error handlers
    register_error_handlers(app)
    
    return app