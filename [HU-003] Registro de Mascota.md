# '[HU-003] Registro de Mascota'

## 📖 Historia de Usuario

Como usuario registrado  
Quiero registrar una mascota en la plataforma  
Para poder almacenar y consultar su información médica y de seguimiento


## 🔁 Flujo Esperado

- El usuario accede al módulo de **registro de mascotas**.  
- El sistema consume el endpoint `/api/mascotas`.  
- El backend valida que el nombre y especie sean campos obligatorios.  
- Se asocia la mascota al usuario autenticado.  
- El sistema almacena la información de la mascota en la base de datos.  
- Se devuelve un mensaje confirmando el registro exitoso.  

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint **POST** `/api/mascotas`.  
- [ ] Se valida que los campos `nombre`, `especie` y `edad` sean requeridos.  
- [ ] Se asocia la mascota al `usuario_id` autenticado.  
- [ ] Se verifica que no exista otra mascota con el mismo nombre asociada al mismo usuario.  

### 2. 📆 Estructura de la información

- [ ] Se recibe la siguiente estructura en JSON:

```json
{
  "nombre": "Firulais",
  "especie": "Perro",
  "raza": "Labrador",
  "edad": 3,
  "peso": 25.5,
  "sexo": "Macho"
}
```

- [ ] Respuesta exitosa:

```json
{
  "mensaje": "Mascota registrada exitosamente",
  "data": {
    "id": 12,
    "nombre": "Firulais",
    "especie": "Perro",
    "raza": "Labrador",
    "edad": 3,
    "peso": 25.5,
    "sexo": "Macho",
    "usuario_id": 1
  },
  "success": true
}
```

- [ ] Si los datos no son válidos, el backend retorna:

```json
{
  "mensaje": "Datos inválidos en la solicitud",
  "error_code": "VALIDATION.FAILED",
  "details": [
    {
      "field": "nombre",
      "message": "El campo nombre es obligatorio"
    },
    {
      "field": "especie",
      "message": "El campo especie es obligatorio"
    }
  ],
  "success": false
}
```

---

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Mascota

- **Método HTTP:** `POST`  
- **Ruta:** `/api/mascotas`  

---

## 📤 Ejemplo de Respuesta JSON

```json
{
  "mensaje": "Mascota registrada exitosamente",
  "data": {
    "id": 12,
    "nombre": "Firulais",
    "especie": "Perro",
    "raza": "Labrador",
    "edad": 3,
    "peso": 25.5,
    "sexo": "Macho",
    "usuario_id": 1
  },
  "success": true
}
```

- [ ] Si los datos son incorrectos:

```json
{
  "mensaje": "Datos inválidos en la solicitud",
  "success": false
}
```

---

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Registro exitoso

- **Precondición:** El usuario está autenticado.  
- **Acción:** Enviar solicitud POST con todos los campos válidos.  
- **Resultado esperado:**  
  - Código HTTP `201 Created`  
  - `success = true`  
  - Mensaje: “Mascota registrada exitosamente”  

---

### ❌ Caso 2: Campos obligatorios faltantes

- **Precondición:** No se envía el campo `nombre` o `especie`.  
- **Acción:** Enviar POST con datos incompletos.  
- **Resultado esperado:**  
  - Código HTTP `400 Bad Request`  
  - Mensaje: “El campo nombre/especie es obligatorio.”  

---

### ❌ Caso 3: Duplicado de mascota

- **Precondición:** Ya existe una mascota con el mismo nombre para el mismo usuario.  
- **Acción:** Ejecutar el endpoint con el mismo nombre.  
- **Resultado esperado:**  
  - Código HTTP `409 Conflict`  
  - Mensaje: “Ya existe una mascota registrada con ese nombre.”  

---

### ❌ Caso 4: Usuario no autenticado

- **Precondición:** No se envía token de autenticación.  
- **Acción:** Ejecutar POST sin encabezado `Authorization`.  
- **Resultado esperado:**  
  - Código HTTP `401 Unauthorized`  
  - Mensaje: “Debe iniciar sesión para registrar una mascota.”  

---

## ✅ Definición de Hecho

## 📦 Alcance Funcional

- [ ] El endpoint permite registrar mascotas válidas.  
- [ ] Se validan los campos obligatorios.  
- [ ] Se evita el registro duplicado por usuario.  
- [ ] El registro queda asociado correctamente al `usuario_id`.  

---

## 🧪 Pruebas Completadas

- [ ] Se probaron registros exitosos y fallas de validación.  
- [ ] Se cubrieron los errores 400, 401 y 409.  
- [ ] Las pruebas unitarias y funcionales pasaron correctamente.  

---

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.  
- [ ] Se describen campos requeridos y ejemplos de respuesta.  

---

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 cuando faltan campos requeridos.  
- [ ] Se devuelve código HTTP 401 si el usuario no está autenticado.  
- [ ] Se devuelve código HTTP 409 cuando la mascota ya existe.  
- [ ] Se devuelve código HTTP 500 ante errores inesperados.  
- [ ] El campo `mensaje` incluye un texto claro y comprensible para el frontend. 
