# README - Migración Completa de Backend a Django

## Resumen del Proceso de Migración

Este proyecto corresponde a la migración total del backend original (Laravel) al framework Django, asegurando equivalencia funcional, seguridad y compatibilidad con el frontend React. Todos los módulos, endpoints, validaciones, lógica avanzada y controles de seguridad han sido replicados y adaptados para mantener la experiencia y funcionamiento original.

---

## Estado Final
- **El backend Django está completamente migrado, seguro y compatible con el frontend.**
- No se ha obviado ningún funcionamiento ni lógica importante de la solución original.
- Todos los endpoints, validaciones, auditoría, seguridad y lógica avanzada están implementados y probados.

---

## Estructura del Proyecto

```
backend/
├── appointments/
├── statuses/
├── tickets/
├── patients/
├── therapists/
├── payment_types/
├── rooms/
├── core/
├── utils/
├── CHECKLIST_MIGRACION.md
├── README_MIGRACION.md
└── db.sqlite3
```

Cada app contiene modelos, formularios, vistas y rutas equivalentes a los del backend original.

---

## Endpoints Principales y Avanzados
- CRUD y lógica avanzada para citas, estados, tickets, pacientes, terapeutas, tipos de pago y habitaciones.
- Endpoints de búsqueda, paginación, calendario, autocompletado, auditoría, cambio de estado, habitaciones/tickets disponibles y estadísticas.
- Soft delete implementado en todos los modelos necesarios.
- Auditoría y control de transiciones de estado disponibles por endpoint.

---

## Seguridad y Permisos
- Todos los endpoints requieren autenticación (token Bearer).
- Permisos granulares por acción y módulo, igual que en Laravel.
- Decoradores y lógica de permisos replican los middlewares originales (`can:...`).

---

## Compatibilidad con el Frontend
- Las rutas y estructura de endpoints son equivalentes y compatibles con el frontend React.
- El frontend puede consumir todos los endpoints usando Axios y tokens Bearer.
- Los mensajes de error y validación son claros y compatibles.
- Las respuestas de la API tienen el formato esperado por el frontend.

---

## Documentación para Verificación de Conexión con el Frontend

### 1. Requisitos Previos
- Tener el entorno virtual de Python activado.
- Instalar dependencias con `pip install -r requirements.txt` (si aplica).
- Ejecutar migraciones con `python manage.py migrate`.
- Iniciar el servidor con `python manage.py runserver` desde la carpeta `backend`.

### 2. Autenticación
- El frontend debe enviar el token Bearer en el header `Authorization` en cada request.
- Si el token es inválido o falta, la API responderá con 401/403.

### 3. Endpoints Disponibles
- `/api/appointments/` (CRUD, búsqueda, paginación, calendario, auditoría, cambio de estado)
- `/api/statuses/` (CRUD, auditoría)
- `/api/tickets/` (tickets y habitaciones disponibles, estadísticas)
- `/api/patients/`, `/api/therapists/`, `/api/payment-types/`, `/api/rooms/` (CRUD y lógica avanzada)

### 4. Mensajes y Formato de Respuesta
- Las respuestas de error y éxito siguen el formato esperado por el frontend.
- Los endpoints devuelven datos en JSON, con claves y estructura equivalentes al backend original.

### 5. Seguridad y Permisos
- Todos los endpoints críticos requieren usuario autenticado y permisos adecuados.
- Los permisos pueden configurarse en el panel de administración de Django (`/admin/`).

### 6. Auditoría y Control de Estado
- El historial de cambios de estado está disponible por endpoint.
- Las transiciones de estado están controladas y solo se permiten las válidas.

### 7. Pruebas y Verificación
- Se recomienda probar todos los endpoints desde el frontend y herramientas como Postman para validar la integración.
- Consultar el archivo `CHECKLIST_MIGRACION.md` para verificar cada punto clave.

---

## Recomendaciones para el Equipo
- Revisar y marcar la checklist antes de poner en producción.
- Consultar este README y la documentación de cada app para dudas técnicas.
- Si se requiere agregar nuevas funcionalidades, seguir la estructura modular y los patrones usados en la migración.

---

**La migración está completa y lista para integración y producción.**
