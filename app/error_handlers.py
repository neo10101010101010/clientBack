from flask import jsonify, current_app

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Solicitud incorrecta',
            'error': str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Recurso no encontrado',
            'error': str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        # Manejar rollback de base de datos de forma segura
        try:
            if hasattr(current_app, 'extensions') and 'sqlalchemy' in current_app.extensions:
                current_app.extensions['sqlalchemy'].db.session.rollback()
        except:
            pass  # Ignorar errores en el rollback durante el manejo de errores
        
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor',
            'error': str(error)
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Manejar rollback de base de datos de forma segura
        try:
            if hasattr(current_app, 'extensions') and 'sqlalchemy' in current_app.extensions:
                current_app.extensions['sqlalchemy'].db.session.rollback()
        except:
            pass  # Ignorar errores en el rollback durante el manejo de errores
        
        return jsonify({
            'success': False,
            'message': 'Error inesperado',
            'error': str(error)
        }), 500