from flask import Flask
from flask_cors import CORS
from .database import init_db
from .error_handlers import register_error_handlers

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Habilitar CORS
    CORS(app)
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Registrar manejadores de errores
    register_error_handlers(app)
    
    return app