-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS turneroAI;
USE turneroAI;

-- Tabla de Paciente
CREATE TABLE IF NOT EXISTS paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255),
    fecha_baja DATETIME NULL
);

-- Tabla de Médico
CREATE TABLE IF NOT EXISTS medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255),
    fecha_baja DATETIME NULL
);

-- Tabla de Especialidad Médica
CREATE TABLE IF NOT EXISTS especialidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_baja DATETIME NULL
);

-- Tabla de Centro de Atención
CREATE TABLE IF NOT EXISTS centro_atencion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_centro VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    es_por_orden_de_llegada BOOLEAN DEFAULT FALSE NOT NULL,
    fecha_baja DATETIME NULL
);

-- Tabla de Consultorio
CREATE TABLE IF NOT EXISTS consultorio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    centro_id INT,
    numero_consultorio VARCHAR(50),
    fecha_baja DATETIME NULL,
    FOREIGN KEY (centro_id) REFERENCES centro_atencion(id) ON DELETE CASCADE
);

-- Tabla de Cita
CREATE TABLE IF NOT EXISTS cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    centro_id INT,
    consultorio_id INT NULL, -- Opcional inicialmente
    fecha_hora DATETIME NOT NULL,
    estado VARCHAR(50),
    practica_id INT,
    fecha_baja DATETIME NULL,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES centro_atencion(id),
    FOREIGN KEY (consultorio_id) REFERENCES consultorio(id) ON DELETE SET NULL,
    FOREIGN KEY (practica_id) REFERENCES practica(id) ON DELETE CASCADE
);

-- Tabla MédicoEspecialidades (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS medico_especialidad (
    medico_id INT,
    especialidad_id INT,
    PRIMARY KEY (medico_id, especialidad_id),
    FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE CASCADE,
    FOREIGN KEY (especialidad_id) REFERENCES especialidad(id) ON DELETE CASCADE
);

-- Tabla MédicoCentros (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS medico_centro (
    medico_id INT,
    centro_id INT,
    PRIMARY KEY (medico_id, centro_id),
    FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES centro_atencion(id) ON DELETE CASCADE
);

-- Tabla Horario Atención
CREATE TABLE IF NOT EXISTS horario_atencion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT,
    centro_id INT,
    dia_semana INT,
    hora_inicio TIME,
    hora_fin TIME,
    fecha_baja DATETIME NULL,
    FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES centro_atencion(id) ON DELETE CASCADE
);

-- Tabla de Práctica
CREATE TABLE IF NOT EXISTS practica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    especialidad_id INT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion_min INT NOT NULL,
    fecha_baja DATETIME NULL,
    FOREIGN KEY (especialidad_id) REFERENCES especialidad(id) ON DELETE CASCADE
);

-- Tabla de Usuario
CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    provider VARCHAR(50),
    provider_id VARCHAR(255),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_baja DATETIME NULL
);

-- Tabla de Rol
CREATE TABLE IF NOT EXISTS rol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla UsuarioRol (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS usuario_rol (
    usuario_id INT,
    rol_id INT,
    PRIMARY KEY (usuario_id, rol_id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE
);

-- Tabla de Productos
CREATE TABLE Productos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10, 2) NOT NULL,
    FechaVigenciaInicio DATE NOT NULL,
    FechaVigenciaFin DATE
);

-- Tabla de Servicios
CREATE TABLE Servicios (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10, 2) NOT NULL,
    FechaVigenciaInicio DATE NOT NULL,
    FechaVigenciaFin DATE
);

-- Tabla de Facturas
CREATE TABLE Facturas (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Fecha DATE NOT NULL,
    Total DECIMAL(10, 2) NOT NULL,
    PacienteID INT,
    Tipo VARCHAR(50),
    CAE VARCHAR(50),
    FechaVencimientoCAE DATE,
    FOREIGN KEY (PacienteID) REFERENCES Pacientes(ID)
);

-- Tabla de Detalle de Factura
CREATE TABLE DetalleFactura (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    FacturaID INT,
    ProductoID INT,
    ServicioID INT,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10, 2) NOT NULL,
    Subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (FacturaID) REFERENCES Facturas(ID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ID),
    FOREIGN KEY (ServicioID) REFERENCES Servicios(ID)
);
