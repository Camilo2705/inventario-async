# Laboratorio Práctico: Sistema de Órdenes de Servicio

## Contexto para los aprendices

Vamos a construir el módulo de recepción y seguimiento de motocicletas de un taller mecánico.

El objetivo es desarrollar una API que permita:

- Registrar las motocicletas que ingresan al taller.
- Consultar las órdenes de servicio existentes.
- Actualizar el estado de reparación.
- Registrar el costo asociado a la reparación.
- Aplicar reglas de negocio antes de modificar la información almacenada.

Para la persistencia de los datos se utilizará un archivo JSON.

## Requisitos generales

El ejercicio debe cumplir con las siguientes condiciones:

- Crear un archivo `taller.json` para almacenar las órdenes.
- Implementar **únicamente 3 endpoints**.
- Utilizar FastAPI.
- Utilizar esquemas Pydantic para validar los datos de entrada.
- Mantener la información persistida en `taller.json`.
- Implementar correctamente las reglas de negocio correspondientes al endpoint `PUT`.

---

# 1. Crear Orden de Ingreso

### Endpoint

```text
POST /ordenes
```

### Esquema de entrada: `OrdenCreate`

El cliente debe enviar los siguientes datos:

| Campo | Tipo | Restricción |
|---|---|---|
| `placa` | `string` | Máximo 6 caracteres |
| `modelo` | `string` | Requerido |
| `falla_reportada` | `string` | Requerido |

Ejemplo conceptual de los datos enviados:

```json
{
    "placa": "ABC123",
    "modelo": "2024",
    "falla_reportada": "No enciende"
}
```

### Lógica del backend

El sistema debe recibir los datos enviados por el cliente y agregar automáticamente los siguientes campos antes de guardar la orden en `taller.json`:

```json
{
    "estado": "En diagnóstico",
    "costo_reparacion": 0
}
```

Por lo tanto, toda nueva orden debe comenzar con:

- **Estado:** `"En diagnóstico"`
- **Costo de reparación:** `0`

### Validación de motocicleta existente

Antes de crear una nueva orden, el backend debe consultar `taller.json` y verificar si ya existe una motocicleta con la misma placa.

Si la placa existe y su estado es diferente de:

```text
Entregada
```

el sistema debe rechazar la solicitud con un error HTTP **400**.

El mensaje debe indicar:

```text
La moto ya se encuentra en el taller
```

Una motocicleta cuyo estado sea `"Entregada"` sí puede volver a ingresar al sistema mediante una nueva orden.

---

# 2. Consultar Órdenes

### Endpoint

```text
GET /ordenes
```

### Lógica del backend

El endpoint debe:

1. Leer el archivo `taller.json`.
2. Obtener todas las órdenes de servicio almacenadas.
3. Devolver la lista completa.
4. Incluir todos los campos registrados para cada orden.

Cada orden debe contener información equivalente a:

```json
{
    "placa": "ABC123",
    "modelo": "2024",
    "falla_reportada": "No enciende",
    "estado": "En diagnóstico",
    "costo_reparacion": 0
}
```

La respuesta debe incluir todas las órdenes almacenadas en el archivo.

---

# 3. Actualizar Diagnóstico y Facturación

### Endpoint

```text
PUT /ordenes/{placa}
```

Este endpoint contiene las principales reglas de negocio del ejercicio.

### Esquema de entrada: `OrdenUpdate`

El cliente debe enviar:

| Campo | Tipo | Descripción |
|---|---|---|
| `nuevo_estado` | `string` | Nuevo estado de la orden |
| `costo_reparacion` | `float` | Costo correspondiente a la reparación |

Ejemplo:

```json
{
    "nuevo_estado": "Reparada",
    "costo_reparacion": 150000
}
```

## Reglas de negocio

### Regla 1: Placa inexistente

Si la placa recibida en la URL no existe en `taller.json`, el backend debe responder con un error HTTP:

```text
404 Not Found
```

La operación no debe modificar ninguna orden existente.

---

### Regla 2: Validación del costo al marcar como reparada

Si el cliente envía:

```text
nuevo_estado = "Reparada"
```

el costo de reparación debe ser **mayor que 0**.

No se permite marcar una motocicleta como reparada sin asignarle un costo de reparación.

Por ejemplo, esta solicitud debe ser rechazada:

```json
{
    "nuevo_estado": "Reparada",
    "costo_reparacion": 0
}
```

El backend debe generar un error HTTP **400** mediante `HTTPException` con el siguiente mensaje:

```text
No se puede marcar como reparada sin asignar un costo de reparación
```

La misma validación debe impedir valores negativos cuando la orden se marca como reparada.

---

### Regla 3: Actualización de la orden

Si la placa existe y todas las validaciones son satisfactorias, el backend debe actualizar en `taller.json`:

- El `estado`.
- El `costo_reparacion`.

Por ejemplo, una actualización válida:

```json
{
    "nuevo_estado": "Reparada",
    "costo_reparacion": 150000
}
```

Debe producir una orden equivalente a:

```json
{
    "placa": "ABC123",
    "modelo": "2024",
    "falla_reportada": "No enciende",
    "estado": "Reparada",
    "costo_reparacion": 150000
}
```

---

# Resumen de endpoints

| Método | Endpoint | Funcionalidad |
|---|---|---|
| `POST` | `/ordenes` | Crear una nueva orden de ingreso |
| `GET` | `/ordenes` | Consultar todas las órdenes |
| `PUT` | `/ordenes/{placa}` | Actualizar estado y costo de reparación |

## Reglas principales

| Situación | Comportamiento esperado |
|---|---|
| Nueva motocicleta | Crear orden con estado `"En diagnóstico"` y costo `0` |
| Placa existente no entregada | HTTP `400` |
| Placa existente con estado `"Entregada"` | Permitir nuevo ingreso |
| Consulta de órdenes | Devolver todas las órdenes |
| Placa inexistente en `PUT` | HTTP `404` |
| Estado `"Reparada"` con costo `0` | HTTP `400` |
| Estado `"Reparada"` con costo negativo | Rechazar la operación |
| Estado `"Reparada"` con costo mayor a `0` | Permitir actualización |
| Actualización válida | Guardar cambios en `taller.json` |