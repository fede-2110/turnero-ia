-- Insertar Pacientes
INSERT INTO paciente (nombre, apellido, dni, fecha_nacimiento, telefono, email) VALUES
('Juan', 'Pérez', '12345678', '1980-05-10', '111-222-3333', 'juan.perez@email.com'),
('Federico', 'Rossi', '33915845', '1988-10-21', '1130422185', 'federico.s.rossi@email.com'),
('Ana', 'García', '23456789', '1975-08-25', '222-333-4444', 'ana.garcia@email.com');

-- Insertar Médicos
INSERT INTO medico (nombre, apellido, telefono, email) VALUES
('Giselle', 'Pignatelli', '1144772354', 'pignatelligiselle@gmail.com');

-- Insertar Especialidades Médicas
INSERT INTO especialidad (nombre_especialidad, descripcion) VALUES
('Dermatología', 'Especialidad médica dedicada al estudio de la piel y sus enfermedades.');

-- Insertar Centros de Atención
INSERT INTO centro_atencion (nombre_centro, direccion, telefono, es_por_orden_de_llegada) VALUES 
('Advanced Skin Center', 'Mitre 114, Lomas de Zamora', '1158478642',0),
('Consultorios Medicos Comunitarios', 'Av. Eva Peron 4265, Monte Chingolo', '1123743406',1),
('Consultorios Integrados San Francisco Solano', 'Av. 844 2762, Solano', '1139020542',1),
('Centro Medico Especializado Lamadrid', 'Mosconi 5, Quilmes', '1158014525',0),
('Consultorios Medicos Bayer', '9 de Julio 1597, Temperley', '1166468195',0),
('Consultorios Medicos El Zorzal', 'El Zorzal 3075, Temperley', '1134383321',1),
('Consultorio Villa Industriales', 'Gobernador Manuel Ocampo 1459, Lanus', '1140982530',1);

-- Relación Médicos-Especialidades
INSERT INTO medico_especialidad (medico_id, especialidad_id) VALUES
(1, 1); -- Asumiendo que Dermatología es el ID 1 en especialidad

-- Relación Médicos-Centros
INSERT INTO medico_centro (medico_id, centro_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7);

-- Insertar Horarios de Atención
INSERT INTO horario_atencion (medico_id, centro_id, dia_semana, hora_inicio, hora_fin) VALUES
(1, 1, 4, '11:00', '19:00'),
(1, 2, 0, '13:00', '14:30'),
(1, 3, 0, '15:00', '18:00'),
(1, 4, 1, '09:00', '12:00'),
(1, 5, 2, '09:00', '16:00'),
(1, 6, 3, '13:30', '15:00'),
(1, 7, 5, '09:00', '12:00');

-- Insertar prácticas
INSERT INTO practica (especialidad_id, nombre, descripcion, duracion_min) VALUES
(1, 'Consulta general', 'Revisión general de dermatología.', 15),
(1, 'Biopsia', 'Biopsia cutanea.', 30);

-- Insertar Citas de ejemplo
INSERT INTO cita (paciente_id, medico_id, centro_id, fecha_hora, estado, practica_id) VALUES
(1, 1, 1, '2024-04-15 09:00:00', 'Confirmada', 1),
(2, 1, 1, '2024-04-16 10:30:00', 'Pendiente', 2);

-- Insertar Roles
INSERT INTO rol (nombre, descripcion) VALUES
('Admin', 'Administrador del sistema'),
('Medico', 'Rol para médicos'),
('Paciente', 'Rol para pacientes');

-- Insertar Usuarios
INSERT INTO usuario (nombre, email, password_hash) VALUES
('admin', 'admin@example.com', '$2b$12$D4G5f18o/MmFpO0hFAF4eO/qiFzr.CV2PMn7ylWuoIjS/ICFob.hG'); -- Password: admin123 (hashed)

-- Relación Usuarios-Roles
INSERT INTO usuario_rol (usuario_id, rol_id) VALUES
(1, 1); -- Asumiendo que el usuario 'admin' es el ID 1 y el rol 'Admin' es el ID 1
