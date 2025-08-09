# Endpoints Utilizables y Ejemplos para Postman

---

## 1. Appointments

### Listar citas
**GET** `/api/appointments/`
```http
GET /api/appointments/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear cita
**POST** `/api/appointments/`
```http
POST /api/appointments/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "appointment_date": "2025-08-10",
  "appointment_hour": "10:00:00",
  "patient": 1,
  "therapist": 2,
  "room": "A",
  "appointment_status": 1
}
```

### Buscar citas
**POST** `/api/appointments/search/`
```http
POST /api/appointments/search/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "search": "Juan",
  "per_page": 10,
  "page": 1
}
```

### Cambiar estado de cita
**POST** `/api/appointments/<id>/change-status/`
```http
POST /api/appointments/5/change-status/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "new_status_id": 2
}
```

---

## 2. Statuses

### Listar estados
**GET** `/api/statuses/`
```http
GET /api/statuses/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear estado
**POST** `/api/statuses/`
```http
POST /api/statuses/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "name": "Confirmada",
  "description": "Cita confirmada"
}
```

---

## 3. Tickets

### Consultar tickets y habitaciones disponibles
**POST** `/api/tickets/available/`
```http
POST /api/tickets/available/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "date": "2025-08-10"
}
```

### Consultar estadísticas
**GET** `/api/tickets/stats/`
```http
GET /api/tickets/stats/
# No se requiere autenticación temporalmente para pruebas locales
```

---

## 4. Patients

### Listar pacientes
**GET** `/api/patients/`
```http
GET /api/patients/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear paciente
**POST** `/api/patients/`
```http
POST /api/patients/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "name": "Juan",
  "paternal_lastname": "Pérez",
  "document_number": "12345678"
}
```

---

## 5. Therapists

### Listar terapeutas
**GET** `/api/therapists/`
```http
GET /api/therapists/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear terapeuta
**POST** `/api/therapists/`
```http
POST /api/therapists/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "name": "Ana",
  "paternal_lastname": "Gómez",
  "document_number": "87654321"
}
```

---

## 6. Payment Types

### Listar tipos de pago
**GET** `/api/payment-types/`
```http
GET /api/payment-types/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear tipo de pago
**POST** `/api/payment-types/`
```http
POST /api/payment-types/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "name": "Efectivo",
  "description": "Pago en efectivo"
}
```

---

## 7. Rooms

### Listar habitaciones
**GET** `/api/rooms/`
```http
GET /api/rooms/
# No se requiere autenticación temporalmente para pruebas locales
```

### Crear habitación
**POST** `/api/rooms/`
```http
POST /api/rooms/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "number": 101,
  "name": "Sala 1"
}
```

### Consultar habitaciones disponibles por fecha
**POST** `/api/rooms/available-by-date/`
```http
POST /api/rooms/available-by-date/
# No se requiere autenticación temporalmente para pruebas locales
Body (JSON):
{
  "date": "2025-08-10"
}
```

---

> Temporalmente, no se requiere autenticación para pruebas locales. Recuerda reactivar los decoradores antes de producción.
