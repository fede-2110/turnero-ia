-- Eliminar tablas de relaciones muchos a muchos primero para evitar conflictos de clave foránea
DROP TABLE IF EXISTS medico_especialidad;
DROP TABLE IF EXISTS medico_centro;
DROP TABLE IF EXISTS horario_atencion;
DROP TABLE IF EXISTS usuario_rol;

-- Ahora, eliminar las tablas que contienen claves foráneas
DROP TABLE IF EXISTS cita;
DROP TABLE IF EXISTS consultorio;

-- Finalmente, eliminar las tablas restantes que solo contienen datos o son referenciadas por otras
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS medico;
DROP TABLE IF EXISTS especialidad;
DROP TABLE IF EXISTS centro_atencion;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS rol;
