## Documento de Validaciones de Servicios

### Introducción
Este documento describe las reglas de validación implementadas en los servicios de la API. Estas validaciones ayudan a asegurar la integridad de los datos y proporcionan retroalimentación clara al usuario sobre los errores de entrada.

### Validaciones Generales
- **Datos no nulos:** Todos los campos marcados como `required` deben estar presentes en la solicitud y no deben ser nulos.
- **Formatos específicos:** Campos como email y DNI deben cumplir con formatos específicos para ser considerados válidos.

### Validaciones Específicas por Entidad

#### Paciente
- **DNI:**
  - Debe ser único en la base de datos.
  - Debe contener solo dígitos y tener una longitud de al menos 6 dígitos.
  - No se puede modificar el DNI de un paciente a uno que ya pertenezca a otro paciente activo.
- **Fecha de Nacimiento:**
  - Debe ser una fecha válida en formato `YYYY-MM-DD`.
  - Debe ser anterior a la fecha actual.
- **Email (opcional):**
  - Si se proporciona, debe ser un email válido.
- **Teléfono (opcional):**
  - Si se proporciona, debe ser un número válido.

#### Modificaciones a Pacientes
- No se puede actualizar ni eliminar un paciente que esté dado de baja.
  - Si se intenta una operación sobre un paciente inactivo, se lanzará un error específico.

### Procedimientos de Validación
Las validaciones se realizan en el servidor, antes de cualquier operación de escritura en la base de datos (crear, actualizar). Esto incluye:
- Cargar los datos recibidos usando el esquema correspondiente.
- Validar los datos contra las reglas establecidas.
- Manejar errores de validación y otros errores inesperados para devolver mensajes claros al cliente.

### Manejo de Errores
Los errores de validación devuelven un código de estado HTTP 400 (Solicitud Incorrecta), acompañados de un mensaje que detalla el problema específico encontrado. Esto permite a los clientes de la API corregir sus solicitudes antes de reintentar.

### Actualizaciones del Documento
Este documento debe ser actualizado cada vez que se modifiquen las reglas de validación o se añadan nuevas entidades y validaciones al sistema.
