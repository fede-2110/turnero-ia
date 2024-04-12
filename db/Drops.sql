-- Eliminar tablas de relaciones muchos a muchos primero para evitar conflictos de clave foránea
DROP TABLE IF EXISTS MedicoEspecialidad;
DROP TABLE IF EXISTS MedicoCentro;
DROP TABLE IF EXISTS HorarioAtencion;

-- Ahora, eliminar las tablas que contienen claves foráneas
DROP TABLE IF EXISTS Cita;
DROP TABLE IF EXISTS Consultorio;

-- Finalmente, eliminar las tablas restantes que solo contienen datos o son referenciadas por otras
DROP TABLE IF EXISTS Paciente;
DROP TABLE IF EXISTS Medico;
DROP TABLE IF EXISTS Especialidad;
DROP TABLE IF EXISTS CentroAtencion;
