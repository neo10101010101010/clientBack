from flask import Blueprint, request, jsonify
from .database import db
from .models import Customer
from .validators import validate_customer_data
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/customers', methods=['GET'])
def get_customers():
    try:
        # Usar SQLAlchemy ORM directamente
        customers = Customer.query.filter_by(status='ACTIVE').order_by(Customer.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [customer.to_dict() for customer in customers],
            'count': len(customers)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener clientes',
            'error': str(e)
        }), 500

@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer = Customer.query.filter_by(id=customer_id, status='ACTIVE').first()
        
        if not customer:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': customer.to_dict()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener cliente',
            'error': str(e)
        }), 500

@api_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        
        # Validar datos
        is_valid, errors = validate_customer_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': 'Datos de entrada inválidos',
                'errors': errors
            }), 400
        
        # Crear nuevo cliente usando ORM
        customer = Customer(
            customer_type=data['customer_type'],
            name=data['name'],
            last_name=data.get('last_name'),
            maternal_last_name=data.get('maternal_last_name'),
            business_name=data.get('business_name'),
            rfc=data['rfc'],
            email=data['email'],
            phone=data['phone']
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'customer_id': customer.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error al crear cliente',
            'error': str(e)
        }), 500

@api_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.get_json()
        
        # Verificar si el cliente existe
        customer = Customer.query.filter_by(id=customer_id, status='ACTIVE').first()
        if not customer:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        # Validar datos
        is_valid, errors = validate_customer_data(data, is_update=True, customer_id=customer_id)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': 'Datos de entrada inválidos',
                'errors': errors
            }), 400
        
        # Actualizar cliente usando ORM
        customer.customer_type = data['customer_type']
        customer.name = data['name']
        customer.last_name = data.get('last_name')
        customer.maternal_last_name = data.get('maternal_last_name')
        customer.business_name = data.get('business_name')
        customer.rfc = data['rfc']
        customer.email = data['email']
        customer.phone = data['phone']
        customer.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente actualizado exitosamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error al actualizar cliente',
            'error': str(e)
        }), 500

@api_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Verificar si el cliente existe
        customer = Customer.query.filter_by(id=customer_id, status='ACTIVE').first()
        if not customer:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
        
        # Borrado lógico
        customer.status = 'INACTIVE'
        customer.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente eliminado exitosamente'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error al eliminar cliente',
            'error': str(e)
        }), 500