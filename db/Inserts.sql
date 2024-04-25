-- Insertar Pacientes
INSERT INTO paciente (nombre, apellido, dni, fecha_nacimiento, telefono, email) VALUES
('Juan', 'Pérez', '12345678', '1980-05-10', '111-222-3333', 'juan.perez@email.com'),
('Federico', 'Rossi', '33915845', '1988-10-21', '1130422185', 'federico.s.rossi@email.com'),
('Ana', 'García', '23456789', '1975-08-25', '222-333-4444', 'ana.garcia@email.com');

-- Insertar Médicos
INSERT INTO medico (nombre, apellido, telefono, email) VALUES
('Laura', 'Martínez', '333-444-5555', 'laura.martinez@email.com'),
('Carlos', 'Rodríguez', '444-555-6666', 'carlos.rodriguez@email.com');

-- Insertar Especialidades Médicas
INSERT INTO especialidad (nombre_especialidad, descripcion) VALUES
('Cardiología', 'Especialidad médica dedicada al diagnóstico y tratamiento de enfermedades del corazón y del sistema circulatorio.'),
('Pediatría', 'Rama de la medicina que involucra el cuidado médico de bebés, niños, y adolescentes.');

-- Insertar Centros de Atención
INSERT INTO centro_atencion (nombre_centro, direccion, telefono) VALUES
('Centro Médico Amanecer', 'Calle Falsa 123, Ciudad Esperanza', '555-666-7777'),
('Clínica Salud y Vida', 'Avenida Siempre Viva 456, Ciudad Sol', '666-777-8888');

-- Insertar Consultorios (opcional)
INSERT INTO consultorio (centro_id, numero_consultorio) VALUES
(1, '101'),
(2, '201');

-- Insertar Citas
INSERT INTO cita (paciente_id, medico_id, centro_id, fecha_hora, estado, motivo_consulta) VALUES
(1, 1, 1, '2024-04-15 09:00:00', 'Confirmada', 'Consulta de rutina'),
(2, 2, 2, '2024-04-16 10:30:00', 'Pendiente', 'Revisión pediátrica');

-- Relación Médicos-Especialidades
INSERT INTO medico_especialidad (medico_id, especialidad_id) VALUES
(1, 1),
(2, 2);

-- Relación Médicos-Centros
INSERT INTO medico_centro (medico_id, centro_id) VALUES
(1, 1),
(2, 2);

-- Insertar Horarios de Atención
INSERT INTO horario_atencion (medico_id, centro_id, dia_semana, hora_inicio, hora_fin) VALUES
(1, 1, 'Lunes', '08:00:00', '12:00:00'),
(1, 1, 'Miércoles', '14:00:00', '18:00:00'),
(2, 2, 'Martes', '09:00:00', '13:00:00'),
(2, 2, 'Jueves', '15:00:00', '19:00:00');
