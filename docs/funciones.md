{
  "name": "create_patient",
  "description": "Creates a new patient record in the database.",
  "parameters": {
    "type": "object",
    "properties": {
      "nombre": {
        "type": "string",
        "description": "First name of the patient"
      },
      "apellido": {
        "type": "string",
        "description": "Last name of the patient"
      },
      "dni": {
        "type": "string",
        "description": "Unique DNI of the patient"
      },
      "fecha_nacimiento": {
        "type": "string",
        "description": "Birthdate of the patient in YYYY-MM-DD format"
      },
      "telefono": {
        "type": "string",
        "description": "Phone number of the patient",
        "optional": true
      },
      "email": {
        "type": "string",
        "description": "Email address of the patient",
        "optional": true
      }
    },
    "required": [
      "nombre",
      "apellido",
      "dni",
      "fecha_nacimiento"
    ]
  }
}

{
  "name": "get_appointment_availability",
  "description": "Checks available appointment slots for a given doctor, center, and practice on a specific date",
  "parameters": {
    "type": "object",
    "properties": {
      "medico_id": {
        "type": "string",
        "description": "The unique identifier of the doctor"
      },
      "centro_id": {
        "type": "string",
        "description": "The unique identifier of the medical center"
      },
      "practica_id": {
        "type": "string",
        "description": "The unique identifier of the practice"
      },
      "date": {
        "type": "string",
        "description": "The requested date for the appointment"
      }
    },
    "required": [
      "medico_id",
      "centro_id",
      "practica_id",
      "date"
    ]
  }
}


{
  "name": "get_available_days",
  "description": "Retrieves available days for appointments with a specific doctor at a specific medical center",
  "parameters": {
    "type": "object",
    "properties": {
      "medico_id": {
        "type": "string",
        "description": "The unique identifier of the doctor"
      },
      "centro_id": {
        "type": "string",
        "description": "The unique identifier of the medical center"
      }
    },
    "required": [
      "medico_id",
      "centro_id"
    ]
  }
}

{
  "name": "get_centers_for_doctor",
  "description": "Lists medical centers where a specific doctor is available",
  "parameters": {
    "type": "object",
    "properties": {
      "medico_id": {
        "type": "string",
        "description": "The unique identifier of the doctor"
      }
    },
    "required": [
      "medico_id"
    ]
  }
}

{
  "name": "fetch_practice_info",
  "description": "Retrieves practice information based on a description and optionally filtered by specialty.",
  "parameters": {
    "type": "object",
    "properties": {
      "practice_description": {
        "type": "string",
        "description": "A descriptive or partial name of the medical practice to search for."
      },
      "specialty_name": {
        "type": "string",
        "description": "The name of the medical specialty to filter the practices. This field is optional but recommended if known."
      }
    },
    "required": [
      "practice_description"
    ]
  }
}

{
  "name": "fetch_patient_info",
  "parameters": {
    "type": "object",
    "properties": {
      "patient_dni": {
        "type": "string",
        "description": "The unique identifier of the patient, typically DNI"
      }
    },
    "required": [
      "patient_dni"
    ]
  },
  "description": "Retrieves patient information using a unique identifier DNI."
}

{
  "name": "fetch_specialty_id",
  "description": "Retrieves the ID of a medical specialty based on its description.",
  "parameters": {
    "type": "object",
    "properties": {
      "specialty_description": {
        "type": "string",
        "description": "The description or part of the description of the specialty."
      }
    },
    "required": [
      "specialty_description"
    ]
  }
}

{
  "name": "fetch_doctors_by_specialty",
  "description": "Retrieves a list of doctors associated with a specific specialty.",
  "parameters": {
    "type": "object",
    "properties": {
      "specialty_id": {
        "type": "string",
        "description": "The unique identifier of the specialty for which doctors are being requested."
      }
    },
    "required": ["specialty_id"]
  }
}

{
  "name": "fetch_current_day",
  "description": "Retrieves the current day of the week from the system.",
  "parameters": {}
}
