-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS customer_management;
USE customer_management;

-- Creación de la tabla customers
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_type ENUM('FISICA', 'MORAL') NOT NULL,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    maternal_last_name VARCHAR(100),
    business_name VARCHAR(200),
    rfc VARCHAR(13) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_rfc (rfc),
    INDEX idx_email (email),
    INDEX idx_status (status)
);

-- Eliminar procedures existentes si los hay
DROP PROCEDURE IF EXISTS sp_get_customers;
DROP PROCEDURE IF EXISTS sp_get_customer_by_id;
DROP PROCEDURE IF EXISTS sp_create_customer;
DROP PROCEDURE IF EXISTS sp_update_customer;
DROP PROCEDURE IF EXISTS sp_delete_customer;

-- Stored Procedure para obtener todos los clientes
DELIMITER //
CREATE PROCEDURE sp_get_customers()
BEGIN
    SELECT 
        id, customer_type, name, last_name, maternal_last_name, 
        business_name, rfc, email, phone, status, created_at, updated_at
    FROM customers 
    WHERE status = 'ACTIVE'
    ORDER BY created_at DESC;
END //
DELIMITER ;

-- Stored Procedure para obtener un cliente por ID
DELIMITER //
CREATE PROCEDURE sp_get_customer_by_id(IN p_customer_id INT)
BEGIN
    SELECT 
        id, customer_type, name, last_name, maternal_last_name, 
        business_name, rfc, email, phone, status, created_at, updated_at
    FROM customers 
    WHERE id = p_customer_id AND status = 'ACTIVE';
END //
DELIMITER ;

-- Stored Procedure para crear un nuevo cliente
DELIMITER //
CREATE PROCEDURE sp_create_customer(
    IN p_customer_type ENUM('FISICA', 'MORAL'),
    IN p_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_maternal_last_name VARCHAR(100),
    IN p_business_name VARCHAR(200),
    IN p_rfc VARCHAR(13),
    IN p_email VARCHAR(120),
    IN p_phone VARCHAR(15)
)
BEGIN
    INSERT INTO customers (
        customer_type, name, last_name, maternal_last_name, 
        business_name, rfc, email, phone
    ) VALUES (
        p_customer_type, p_name, p_last_name, p_maternal_last_name,
        p_business_name, p_rfc, p_email, p_phone
    );
END //
DELIMITER ;

-- Stored Procedure para actualizar un cliente
DELIMITER //
CREATE PROCEDURE sp_update_customer(
    IN p_customer_id INT,
    IN p_customer_type ENUM('FISICA', 'MORAL'),
    IN p_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_maternal_last_name VARCHAR(100),
    IN p_business_name VARCHAR(200),
    IN p_rfc VARCHAR(13),
    IN p_email VARCHAR(120),
    IN p_phone VARCHAR(15)
)
BEGIN
    UPDATE customers 
    SET 
        customer_type = p_customer_type,
        name = p_name,
        last_name = p_last_name,
        maternal_last_name = p_maternal_last_name,
        business_name = p_business_name,
        rfc = p_rfc,
        email = p_email,
        phone = p_phone,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_customer_id;
END //
DELIMITER ;

-- Stored Procedure para eliminar un cliente (borrado lógico)
DELIMITER //
CREATE PROCEDURE sp_delete_customer(IN p_customer_id INT)
BEGIN
    UPDATE customers 
    SET status = 'INACTIVE', updated_at = CURRENT_TIMESTAMP
    WHERE id = p_customer_id;
END //
DELIMITER ;

-- Insertar datos de ejemplo
INSERT INTO customers (customer_type, name, last_name, maternal_last_name, business_name, rfc, email, phone) VALUES
('FISICA', 'Juan', 'Pérez', 'Gómez', NULL, 'PEGJ800101ABC', 'juan.perez@example.com', '5512345678'),
('FISICA', 'María', 'López', 'Hernández', NULL, 'LOHM850505DEF', 'maria.lopez@example.com', '5512345679'),
('MORAL', NULL, NULL, NULL, 'Empresa ABC S.A. de C.V.', 'ABC123456789', 'empresa@example.com', '5512345600');

-- Mostrar mensaje de confirmación
SELECT 'Base de datos, tabla y stored procedures creados exitosamente!' as Status;