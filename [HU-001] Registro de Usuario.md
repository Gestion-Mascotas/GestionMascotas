# '[HU-001] Registro de Usuario'

## 📖 Historia de Usuario

Como nuevo usuario (dueño o veterinario)
Quiero registrarme en la plataforma
Para poder acceder y gestionar la información de las mascotas

## 🔁 Flujo Esperado

- El usuario ingresa sus datos en el formulario de registro.  
- El sistema consume el endpoint `/api/usuarios`.  
- El backend valida que el correo tenga formato correcto y no exista previamente.  
- El sistema cifra la contraseña antes de almacenarla en la base de datos.  
- Se asigna el rol correspondiente (dueño o veterinario).  
- El sistema devuelve un mensaje confirmando el registro exitoso. 


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint **POST** `/api/usuarios`.  
- [ ] Se valida que el campo `correo` tenga un formato válido y no esté duplicado.  
- [ ] Se encripta la contraseña antes de almacenarla.  
- [ ] Se asigna un rol válido entre: `dueño`, `veterinario`, `admin`. 


### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON:

```json
{
  "nombre": "Juan Pérez",
  "correo": "juan@example.com",
  "contraseña": "12345678",
  "rol": "dueño"
}
```

- [ ] Respuesta exitosa:

```json
{
  "mensaje": "Usuario creado exitosamente",
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "rol": "dueño"
  },
  "success": true
}
```

- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "Datos inválidos en la solicitud",
  "error_code": "VALIDATION.FAILED",
  "details": [
    {
      "field": "correo",
      "message": "El correo ya está registrado"
    },
    {
      "field": "contraseña",
      "message": "Debe tener al menos 8 caracteres"
    }
  ],
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Usuario

- **Método HTTP:** `POST`
- **Ruta:** `/api/usuarios `

## 📤 Ejemplo de Respuesta JSON

````json
{
  "mensaje": "Usuario creado exitosamente",
  "data": {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "rol": "dueño"
  },
  "success": true
}

````

- [ ] Si no existen datos, el backend retorna:

```json
{
  "mensaje": "Datos inválidos en la solicitud",
  "success": false
}
```

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Registro exitoso

- **Precondición:** El correo no está registrado.
- **Acción:** Enviar solicitud POST con datos válidos.
- **Resultado esperado:**

  - Código HTTP `201 Created`
  - `success = true`
  - Mensaje: “Usuario creado exitosamente”

  ### ❌ Caso 2: Correo duplicado

- **Precondición:** : Ya existe un usuario con el mismo correo.
- **Acción:** Ejecutar el endpoint con correo repetido.
- **Resultado esperado:**
  - Código HTTP `409 Conflict`
  - Mensaje: “El correo ya está registrado”.

### ❌ Caso 3: Contraseña corta 

- **Precondición:** Contraseña menor a 8 caracteres.
- **Acción:** Enviar POST con `"contraseña": "1234"`.
- **Resultado esperado:**
  - Código HTTP `400 Bad Request`
  - Mensaje: “La contraseña debe tener al menos 8 caracteres”.

  ### ❌ Caso 4: Correo con formato inválido

- **Precondición:** Correo con error de formato.
- **Acción:** Enviar `"correo": "juan@@example"`.
- **Resultado esperado:**
  - Código HTTP `400 Bad Request`
  - Mensaje: “El correo no tiene un formato válido”.

## ✅ Definición de Hecho

#Historia: Consulta del Último Cierre Procesado

## 📦 Alcance Funcional

- [ ] El endpoint permite crear un usuario con datos válidos.
- [ ] Las validaciones de correo y contraseña están activas.
- [ ] Las contraseñas se almacenan cifradas.
- [ ] El rol asignado es válido.

  ## 🧪 Pruebas Completadas

- [ ] Se probaron registros exitosos y errores de validación.
- [ ] Se cubrieron los casos de error 400 y 409.
- [ ] Las pruebas unitarias y funcionales pasaron correctamente.

  ## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describen campos, roles y ejemplos de respuesta.

  ## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 cuando los datos son inválidos.
- [ ] Se devuelve código HTTP 409 cuando el correo ya existe.
- [ ] Se devuelve código HTTP 500 cuando ocurre un error inesperado en el servidor.
- [ ] El campo `mensaje` en el JSON incluye un texto amigable y claro para el usuario técnico o frontend.
