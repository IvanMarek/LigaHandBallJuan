-- Borrar la base de datos actual si existe
DROP DATABASE IF EXISTS `LigaHandball`;

-- Crear la base de datos
CREATE DATABASE LigaHandball;
USE LigaHandball;

-- Crear la tabla de Localidades
CREATE TABLE Localidades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Crear la tabla de Géneros
CREATE TABLE Generos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Crear la tabla de Clubes
CREATE TABLE Clubes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    genero_id INT NOT NULL,
    localidad_id INT NOT NULL,
    logo VARCHAR(255),  -- Almacena la ruta del archivo del logo
    FOREIGN KEY (genero_id) REFERENCES Generos(id),
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    UNIQUE (nombre, genero_id, localidad_id) -- Restricción única para distinguir clubes por nombre, género y localidad
);

-- Crear la tabla de Jugadores
CREATE TABLE Jugadores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(10) NOT NULL UNIQUE,  -- Limitar a 10 caracteres para evitar datos inconsistentes
    correo_electronico VARCHAR(100) UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    genero_id INT NOT NULL,
    localidad_id INT NOT NULL,
    club_id INT,
    ficha_medica_activa BOOLEAN NOT NULL DEFAULT 0,  -- Indicador de ficha médica activa
    carnet VARCHAR(255),  -- Almacena la ruta del archivo del carnet
    FOREIGN KEY (genero_id) REFERENCES Generos(id),
    FOREIGN KEY (localidad_id) REFERENCES Localidades(id),
    FOREIGN KEY (club_id) REFERENCES Clubes(id)
);

-- Insertar datos en la tabla Localidades
INSERT INTO Localidades (nombre) VALUES 
('Bialet Massé'), 
('Capilla del Monte'), 
('Cosquín (cabecera)'), 
('Huerta Grande'), 
('La Cumbre'), 
('La Falda'), 
('Los Cocos'), 
('San Antonio de Arredondo'), 
('San Esteban'), 
('Santa María'), 
('Tanti'), 
('Valle Hermoso'), 
('Villa Carlos Paz'), 
('Villa Giardino'), 
('Villa Icho Cruz'), 
('Villa Santa Cruz del Lago'), 
('Cabalango'), 
('Casa Grande'), 
('Charbonier'), 
('Cuesta Blanca'), 
('Estancia Vieja'), 
('Mayu Sumaj'), 
('San Roque'), 
('Tala Huasi'), 
('Villa Parque Siquiman'), 
('Malagueño'), 
('Córdoba Capital'),
('Villa Saldán'); -- Nueva localidad

-- Insertar datos en la tabla Generos
INSERT INTO Generos (descripcion) VALUES 
('Masculino'),
('Femenino');

-- Insertar datos en la tabla Clubes
-- Clubes femeninos
INSERT INTO Clubes (nombre, genero_id, localidad_id) VALUES
('Municipalidad Malagueño', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño')),
('Club Sarmiento', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz')),
('Zona Sur (Córdoba Capital)', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital')),
('Universitario Cosquín', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)')),
('Unión Huerta Grande', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Huerta Grande')),
('Club Capilla del Monte', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Capilla del Monte')),
('Polideportivo Ampliación Matienzo', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital')),
('Club Villa Azalain', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital'));

-- Clubes masculinos
INSERT INTO Clubes (nombre, genero_id, localidad_id) VALUES
('Universitario Cosquín', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)')),
('Unión Huerta Grande', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Huerta Grande')),
('Municipalidad Malagueño', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño')),
('Club Sarmiento', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz')),
('Zona Sur (Córdoba Capital)', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Córdoba Capital')),
('Club Capilla del Monte', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Capilla del Monte')),
('Municipalidad Saldan', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Saldán'));

-- Insertar algunos jugadores de ejemplo
INSERT INTO Jugadores (nombre, apellido, dni, correo_electronico, fecha_nacimiento, genero_id, localidad_id, club_id) VALUES
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', '1995-05-15', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Bialet Massé'), 1),
('Maria', 'González', '87654321', 'maria.gonzalez@example.com', '1998-08-22', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Villa Carlos Paz'), 2),
('Luis', 'Martínez', '11223344', 'luis.martinez@example.com', '2002-03-30', (SELECT id FROM Generos WHERE descripcion = 'Masculino'), (SELECT id FROM Localidades WHERE nombre = 'Cosquín (cabecera)'), 3),
('Ana', 'Lopez', '44332211', 'ana.lopez@example.com', '1999-11-11', (SELECT id FROM Generos WHERE descripcion = 'Femenino'), (SELECT id FROM Localidades WHERE nombre = 'Malagueño'), 4);