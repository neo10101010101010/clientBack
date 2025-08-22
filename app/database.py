from flask_sqlalchemy import SQLAlchemy
import pymysql

# Usar PyMySQL como driver de MySQL
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas si no existen
        db.create_all()
        
        # Verificar que la tabla customers existe
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'customers' not in inspector.get_table_names():
            print(" La tabla 'customers' no existe, creándola... ")
            # Forzar la creación de tablas
            from .models import Customer
            db.create_all()