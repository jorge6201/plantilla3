
-- Hacemos la conexion a la base de datos con esta instruccion
--mysql -u root -p
--Enter password: *********


SHOW DATABASES;
CREATE DATABASE users_db;
USE users_db;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  password VARCHAR(100), 
  rol VARCHAR(10) DEFAULT 'usuario'
);

-- Este script muestra las tablas de la base de datos
SHOW TABLES;

-- Este script hace un volcado de la tabla de usuarios
SELECT * FROM users;

-- Este script muestra la estructura de la tabla de usuarios
DESCRIBE users;

-- Este script modifica la tabla de usuarios para agregar un campo de rol y ajustar el campo de contraseña
ALTER TABLE users MODIFY password VARCHAR(255);

-- Agregar el campo de rol a la tabla de usuarios
ALTER TABLE users ADD  rol VARCHAR(10);

-- Modificar el campo de rol para que sea no nulo y ajustar su posición
ALTER TABLE users MODIFY rol VARCHAR(10) AFTER id;

-- Limpiar la consola de comandos
SYSTEM cls

-- Este script muestra los usuarios que no tienen rol asignado
SELECT * FROM users WHERE rol IS NULL;

-- Este script actualiza los usuarios que no tienen rol asignado a 'usuario'
UPDATE users SET rol = 'usuario' WHERE rol IS NULL;

-- Este script actualiza los usuarios que tienen rol 'string' a 'usuario'
UPDATE users SET rol = 'usuario' WHERE rol = 'string';

