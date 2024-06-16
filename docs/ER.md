# 📚 Modelo de Entidad-Relación para TurneroAI

## 📄 Entidades y Atributos

#### 🧑‍⚕️ Pacientes

| Campo               | Tipo                         | Descripción                               |
|---------------------|------------------------------|-------------------------------------------|
| `Id`                | INT AUTO_INCREMENT (PK)      | Identificador único del paciente          |
| `Nombre`            | VARCHAR(255)                 | Nombre del paciente                       |
| `Apellido`          | VARCHAR(255)                 | Apellido del paciente                     |
| `DNI`               | VARCHAR(20) UNIQUE           | Documento Nacional de Identidad (único)   |
| `FechaDeNacimiento` | DATE                         | Fecha de nacimiento del paciente          |
| `Telefono`          | VARCHAR(20)                  | Teléfono de contacto                      |
| `Email`             | VARCHAR(255)                 | Correo electrónico                        |
| `FechaBaja`         | DATETIME NULL                | Fecha de baja lógica (soft delete)        |

#### 👨‍⚕️ Medicos

| Campo       | Tipo                         | Descripción                           |
|-------------|------------------------------|---------------------------------------|
| `Id`        | INT AUTO_INCREMENT (PK)      | Identificador único del médico        |
| `Nombre`    | VARCHAR(255)                 | Nombre del médico                     |
| `Apellido`  | VARCHAR(255)                 | Apellido del médico                   |
| `Telefono`  | VARCHAR(20)                  | Teléfono de contacto                  |
| `Email`     | VARCHAR(255)                 | Correo electrónico                    |
| `FechaBaja` | DATETIME NULL                | Fecha de baja lógica (soft delete)    |

#### 🎓 Especialidades

| Campo              | Tipo                         | Descripción                               |
|--------------------|------------------------------|-------------------------------------------|
| `Id`               | INT AUTO_INCREMENT (PK)      | Identificador único de la especialidad    |
| `NombreEspecialidad` | VARCHAR(255)               | Nombre de la especialidad médica          |
| `Descripcion`      | TEXT                         | Descripción de la especialidad            |
| `FechaBaja`        | DATETIME NULL                | Fecha de baja lógica (soft delete)        |

#### 🏥 CentrosAtencion

| Campo         | Tipo                         | Descripción                               |
|---------------|------------------------------|-------------------------------------------|
| `Id`          | INT AUTO_INCREMENT (PK)      | Identificador único del centro de atención|
| `NombreCentro`| VARCHAR(255)                 | Nombre del centro de atención             |
| `Direccion`   | VARCHAR(255)                 | Dirección física del centro               |
| `Telefono`    | VARCHAR(20)                  | Teléfono de contacto                      |
| `EsPorOrdenDeLlegada` | BOOLEAN              | Indica si la atención es por orden de llegada |
| `FechaBaja`   | DATETIME NULL                | Fecha de baja lógica (soft delete)        |

#### 🚪 Consultorios

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `Id`             | INT AUTO_INCREMENT (PK)      | Identificador único del consultorio       |
| `CentroId`       | INT (FK a CentrosAtencion)   | Identificador del centro de atención      |
| `NumeroConsultorio` | VARCHAR(50)              | Número o código del consultorio           |
| `FechaBaja`      | DATETIME NULL                | Fecha de baja lógica (soft delete)        |

#### 📅 Citas

| Campo           | Tipo                           | Descripción                         |
|-----------------|--------------------------------|-------------------------------------|
| `Id`            | INT AUTO_INCREMENT (PK)        | Identificador único de la cita      |
| `PacienteId`    | INT (FK a Pacientes)           | Identificador del paciente          |
| `MedicoId`      | INT (FK a Medicos)             | Identificador del médico            |
| `CentroId`      | INT (FK a CentrosAtencion)     | Identificador del centro de atención|
| `ConsultorioId` | INT NULL (FK a Consultorios)   | Identificador del consultorio (opcional) |
| `FechaHora`     | DATETIME                       | Fecha y hora de la cita             |
| `Estado`        | VARCHAR(50)                    | Estado de la cita (p.ej., confirmada, pendiente) |
| `MotivoConsulta`| TEXT                           | Motivo de la consulta               |
| `FechaBaja`     | DATETIME NULL                  | Fecha de baja lógica (soft delete)  |

#### 👨‍⚕️🤝🎓 MedicosEspecialidades (Relación Muchos a Muchos entre Medicos y Especialidades)

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `MedicoId`       | INT (FK a Medicos)           | Identificador del médico                  |
| `EspecialidadId` | INT (FK a Especialidades)    | Identificador de la especialidad          |

#### 👨‍⚕️🤝🏥 MedicosCentros (Relación Muchos a Muchos entre Medicos y CentrosAtencion)

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `MedicoId`       | INT (FK a Medicos)           | Identificador del médico                  |
| `CentroId`       | INT (FK a CentrosAtencion)   | Identificador del centro de atención      |

#### 🕒 HorariosAtencion

| Campo        | Tipo                        | Descripción                        |
|--------------|-----------------------------|------------------------------------|
| `Id`         | INT AUTO_INCREMENT (PK)     | Identificador único del horario de atención |
| `MedicoId`   | INT (FK a Medicos)          | Identificador del médico           |
| `CentroId`   | INT (FK a CentrosAtencion)  | Identificador del centro de atención |
| `DiaSemana`  | INT                         | Día de la semana                   |
| `HoraInicio` | TIME                        | Hora de inicio de la atención      |
| `HoraFin`    | TIME                        | Hora de fin de la atención         |
| `FechaBaja`  | DATETIME NULL               | Fecha de baja lógica (soft delete) |

#### 🧑‍💻 Usuarios

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `Id`             | INT AUTO_INCREMENT (PK)      | Identificador único del usuario           |
| `Nombre`         | VARCHAR(255)                 | Nombre del usuario                        |
| `Email`          | VARCHAR(255) UNIQUE          | Correo electrónico del usuario            |
| `PasswordHash`   | VARCHAR(255)                 | Hash de la contraseña del usuario         |
| `Provider`       | VARCHAR(50)                  | Proveedor de autenticación (ej. google, facebook) |
| `ProviderId`     | VARCHAR(255)                 | Identificador del proveedor               |
| `FechaCreacion`  | DATETIME DEFAULT CURRENT_TIMESTAMP | Fecha de creación del usuario    |
| `FechaBaja`      | DATETIME NULL                | Fecha de baja lógica (soft delete)        |

#### 🔐 Roles

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `Id`             | INT AUTO_INCREMENT (PK)      | Identificador único del rol               |
| `Nombre`         | VARCHAR(50) UNIQUE           | Nombre del rol                            |
| `Descripcion`    | TEXT                         | Descripción del rol                       |

#### 🧑‍💻🤝🔐 UsuarioRoles (Relación Muchos a Muchos entre Usuarios y Roles)

| Campo            | Tipo                         | Descripción                               |
|------------------|------------------------------|-------------------------------------------|
| `UsuarioId`      | INT (FK a Usuarios)          | Identificador del usuario                 |
| `RolId`          | INT (FK a Roles)             | Identificador del rol                     |

## 🔗 Relaciones

- **🧑‍⚕️ Pacientes** a **📅 Citas**: Uno a muchos (1:N)
- **👨‍⚕️ Medicos** a **📅 Citas**: Uno a muchos (1:N)
- **🏥 CentrosAtencion** a **🚪 Consultorios**: Uno a muchos (1:N)
- **🏥 CentrosAtencion** a **📅 Citas**: Uno a muchos (1:N)
- **🚪 Consultorios** a **📅 Citas**: Uno a muchos (1:N, opcional)
- **👨‍⚕️ Medicos** a **🎓 Especialidades**: Muchos a muchos (N:M)
- **👨‍⚕️ Medicos** a **🏥 CentrosAtencion**: Muchos a muchos (N:M)
- **👨‍⚕️ Medicos** a **🕒 HorariosAtencion**: Uno a muchos (1:N)
- **🧑‍💻 Usuarios** a **🔐 Roles**: Muchos a muchos (N:M)
