-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS turneroAI;
USE turneroAI;

-- Tabla de Pacientes
CREATE TABLE IF NOT EXISTS Pacientes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Apellido VARCHAR(255) NOT NULL,
    DNI VARCHAR(20) UNIQUE NOT NULL,
    FechaDeNacimiento DATE NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(255),
    FechaBaja DATETIME NULL
);

-- Tabla de Médicos
CREATE TABLE IF NOT EXISTS Medicos (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Apellido VARCHAR(255) NOT NULL,
    Telefono VARCHAR(20),
    Email VARCHAR(255),
    FechaBaja DATETIME NULL
);

-- Tabla de Especialidades Médicas
CREATE TABLE IF NOT EXISTS Especialidades (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    NombreEspecialidad VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    FechaBaja DATETIME NULL
);

-- Tabla de Centros de Atención
CREATE TABLE IF NOT EXISTS CentrosAtencion (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    NombreCentro VARCHAR(255) NOT NULL,
    Direccion VARCHAR(255) NOT NULL,
    Telefono VARCHAR(20),
    FechaBaja DATETIME NULL
);

-- Tabla de Consultorios
CREATE TABLE IF NOT EXISTS Consultorios (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    CentroId INT,
    NumeroConsultorio VARCHAR(50),
    FechaBaja DATETIME NULL,
    FOREIGN KEY (CentroId) REFERENCES CentrosAtencion(Id) ON DELETE CASCADE
);

-- Tabla de Citas
CREATE TABLE IF NOT EXISTS Citas (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    PacienteId INT,
    MedicoId INT,
    CentroId INT,
    ConsultorioId INT NULL, -- Opcional inicialmente
    FechaHora DATETIME NOT NULL,
    Estado VARCHAR(50),
    MotivoConsulta TEXT,
    FechaBaja DATETIME NULL,
    FOREIGN KEY (PacienteId) REFERENCES Pacientes(Id) ON DELETE CASCADE,
    FOREIGN KEY (MedicoId) REFERENCES Medicos(Id) ON DELETE CASCADE,
    FOREIGN KEY (CentroId) REFERENCES CentrosAtencion(Id),
    FOREIGN KEY (ConsultorioId) REFERENCES Consultorios(Id) ON DELETE SET NULL
);

-- Tabla MédicosEspecialidades (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS MedicosEspecialidades (
    MedicoId INT,
    EspecialidadId INT,
    PRIMARY KEY (MedicoId, EspecialidadId),
    FOREIGN KEY (MedicoId) REFERENCES Medicos(Id) ON DELETE CASCADE,
    FOREIGN KEY (EspecialidadId) REFERENCES Especialidades(Id) ON DELETE CASCADE
);

-- Tabla MédicosCentros (Relación Muchos a Muchos)
CREATE TABLE IF NOT EXISTS MedicosCentros (
    MedicoId INT,
    CentroId INT,
    PRIMARY KEY (MedicoId, CentroId),
    FOREIGN KEY (MedicoId) REFERENCES Medicos(Id) ON DELETE CASCADE,
    FOREIGN KEY (CentroId) REFERENCES CentrosAtencion(Id) ON DELETE CASCADE
);

-- Tabla Horarios Atención
CREATE TABLE IF NOT EXISTS HorariosAtencion (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    MedicoId INT,
    CentroId INT,
    DiaSemana VARCHAR(10),
    HoraInicio TIME,
    HoraFin TIME,
    FechaBaja DATETIME NULL,
    FOREIGN KEY (MedicoId) REFERENCES Medicos(Id) ON DELETE CASCADE,
    FOREIGN KEY (CentroId) REFERENCES CentrosAtencion(Id) ON DELETE CASCADE
);
