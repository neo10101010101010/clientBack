from datetime import datetime
from .database import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_type = db.Column(db.Enum('FISICA', 'MORAL'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))  # Solo para personas físicas
    maternal_last_name = db.Column(db.String(100))  # Solo para personas físicas
    business_name = db.Column(db.String(200))  # Solo para personas morales
    rfc = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Enum('ACTIVE', 'INACTIVE'), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_type': self.customer_type,
            'name': self.name,
            'last_name': self.last_name,
            'maternal_last_name': self.maternal_last_name,
            'business_name': self.business_name,
            'rfc': self.rfc,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }