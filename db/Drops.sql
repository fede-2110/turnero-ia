-- Eliminar tablas de relaciones muchos a muchos primero para evitar conflictos de clave foránea
DROP TABLE IF EXISTS MedicosEspecialidades;
DROP TABLE IF EXISTS MedicosCentros;
DROP TABLE IF EXISTS HorariosAtencion;

-- Ahora, eliminar las tablas que contienen claves foráneas
DROP TABLE IF EXISTS Citas;
DROP TABLE IF EXISTS Consultorios;

-- Finalmente, eliminar las tablas restantes que solo contienen datos o son referenciadas por otras
DROP TABLE IF EXISTS Pacientes;
DROP TABLE IF EXISTS Medicos;
DROP TABLE IF EXISTS Especialidades;
DROP TABLE IF EXISTS CentrosAtencion;
