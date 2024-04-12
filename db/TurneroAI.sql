-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS turneroAI;
USE turneroAI;

-- Tabla de Paciente
CREATE TABLE IF NOT EXISTS Paciente (
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
CREATE TABLE IF NOT EXISTS Medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255),
    fecha_baja DATETIME NULL
);

-- Tabla de Especialidad Médica
CREATE TABLE IF NOT EXISTS Especialidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_baja DATETIME NULL
);

-- Tabla de Centro de Atención
CREATE TABLE IF NOT EXISTS CentroAtencion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_centro VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_baja DATETIME NULL
);

-- Tabla de Consultorio
CREATE TABLE IF NOT EXISTS Consultorio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    centro_id INT,
    numero_consultorio VARCHAR(50),
    fecha_baja DATETIME NULL,
    FOREIGN KEY (centro_id) REFERENCES CentroAtencion(id) ON DELETE CASCADE
);

-- Tabla de Cita
CREATE TABLE IF NOT EXISTS Cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    medico_id INT,
    centro_id INT,
    consultorio_id INT NULL, -- Opcional inicialmente
    fecha_hora DATETIME NOT NULL,
    estado VARCHAR(50),
    motivo_consulta TEXT,
    fecha_baja DATETIME NULL,
    FOREIGN KEY (paciente_id) REFERENCES Paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (medico_id) REFERENCES Medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES CentroAtencion(id),
    FOREIGN KEY (consultorio_id) REFERENCES Consultorio(id) ON DELETE SET NULL
);

-- Tabla MédicoEspecialidades (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS MedicoEspecialidad (
    medico_id INT,
    especialidad_id INT,
    PRIMARY KEY (medico_id, especialidad_id),
    FOREIGN KEY (medico_id) REFERENCES Medico(id) ON DELETE CASCADE,
    FOREIGN KEY (especialidad_id) REFERENCES Especialidad(id) ON DELETE CASCADE
);

-- Tabla MédicoCentros (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS MedicoCentro (
    medico_id INT,
    centro_id INT,
    PRIMARY KEY (medico_id, centro_id),
    FOREIGN KEY (medico_id) REFERENCES Medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES CentroAtencion(id) ON DELETE CASCADE
);

-- Tabla Horario Atención
CREATE TABLE IF NOT EXISTS HorarioAtencion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT,
    centro_id INT,
    dia_semana VARCHAR(10),
    hora_inicio TIME,
    hora_fin TIME,
    fecha_baja DATETIME NULL,
    FOREIGN KEY (medico_id) REFERENCES Medico(id) ON DELETE CASCADE,
    FOREIGN KEY (centro_id) REFERENCES CentroAtencion(id) ON DELETE CASCADE
);
