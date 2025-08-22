import pytest
from app.validators import validate_rfc, validate_email, validate_phone

def test_validate_rfc(app):
    with app.app_context():
        assert validate_rfc('MABC800101ABC', 'FISICA')[0] == True
        assert validate_rfc('ABC800101ABC', 'MORAL')[0] == True

        is_valid, message = validate_rfc('ABC800101AB', 'FISICA')
        assert is_valid == False
        assert '13 caracteres' in message

        is_valid, message = validate_rfc('MABC800101ABC', 'MORAL')
        assert is_valid == False
        assert '12 caracteres' in message

        is_valid, message = validate_rfc('1234567890123', 'FISICA')
        assert is_valid == False
        assert 'Formato de RFC inválido' in message

def test_validate_email(app):
    with app.app_context():
        assert validate_email('test@example.com')[0] == True

        is_valid, message = validate_email('invalid-email')
        assert is_valid == False
        assert 'Formato de email inválido' in message

def test_validate_phone():
    # Teléfono válido
    assert validate_phone('5512345678')[0] == True
    
    # Teléfono con letras
    is_valid, message = validate_phone('55abc56789')
    assert is_valid == False
    assert 'dígitos' in message
    
    # Teléfono demasiado corto
    is_valid, message = validate_phone('123')
    assert is_valid == False
    assert 'dígitos' in message