# '[HU-002] AUTENTICACIÓN DE USUARIO'

## 📖 Historia de Usuario

Como usuario registrado
Quiero iniciar sesión en el sistema
Para acceder a la información de mis mascotas y su historial médico

## 🔁 Flujo Esperado

- El usuario ingresa su correo y contraseña en el formulario de inicio de sesión.
- El sistema consume el endpoint `/api/login`.
- El backend valida que el correo exista y la contraseña coincida con la almacenada (verificada tras el cifrado).
- Si la autenticación es exitosa, el sistema genera un token JWT.
- El backend retorna el token junto con los datos básicos del usuario autenticado. 


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint **POST** `/api/login`.
- [ ] Se valida la existencia del correo electrónico en la base de datos.  
- [ ] Se valida la contraseña mediante comparación segura.  
- [ ] Se genera un token JWT con tiempo de expiración definido.  
- [ ] Se devuelve la información básica del usuario autenticado.


### 2. 📆 Estructura de la información

- [ ] La solicitud debe tener el siguiente formato:

```json
{
  "correo": "juan@example.com",
  "contraseña": "12345678"
}
```

- [ ] Respuesta exitosa:

```json
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "token": "jwt-token-generado",
    "usuario": {
      "id": 1,
      "nombre": "Juan Pérez",
      "correo": "juan@example.com",
      "rol": "dueño"
    }
  },
  "success": true
}

```

- [ ] Si las credenciales son incorrectas:

```json
{
  "mensaje": "Correo o contraseña incorrectos",
  "success": false
}
```

- [ ] Si el usuario no existe

```json
{
  "mensaje": "El usuario no está registrado",
  "success": false
}
```

## 🔧 Notas Técnicas

## 🚀 Endpoint – Autenticación de Usuario

- **Método HTTP:** `POST`
- **Ruta:** `/api/login `

## 📤 Ejemplo de Respuesta JSON

````json
{
  "mensaje": "Inicio de sesión exitoso",
  "data": {
    "token": "jwt-token-generado",
    "usuario": {
      "id": 1,
      "nombre": "Juan Pérez",
      "correo": "juan@example.com",
      "rol": "dueño"
    }
  },
  "success": true
}
````

- [ ] Si las credenciales no son válidas:

```json

{
  "mensaje": "Correo o contraseña incorrectos",
  "success": false
}

````


## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Autenticación exitosa

- **Precondición:** El usuario existe y la contraseña es correcta.
- **Acción:** Enviar solicitud `POST /api/login` con credenciales válidas.
- **Resultado esperado:**

  - Código HTTP `200 OK`
  - Se retorna token JWT y datos del usuario.
  - `success = true`


  ### ❌ Caso 2: Usuario no existente

- **Precondición:** : El correo no está registrado en la base de datos.
- **Acción:** Enviar solicitud `POST /api/login`.
- **Resultado esperado:**
  - Código HTTP `404 Not Found`
  - `success = false`
  - Mensaje: “El usuario no está registrado.”.

### ❌ Caso 3: Contraseña incorrecta

- **Precondición:** El correo existe, pero la contraseña no coincide.
- **Acción:** Enviar solicitud `POST /api/login`.
- **Resultado esperado:**
  - Código HTTP `401 Unauthorized`
  - Mensaje: “Correo o contraseña incorrectos”.

  ### ❌ Caso 4: Campos faltantes

- **Precondición:** El usuario no envía correo o contraseña.
- **Acción:** Enviar JSON incompleto.
- **Resultado esperado:**
  - Código HTTP `400 Bad Request`
  - Mensaje: “Faltan campos obligatorios”.

## ✅ Definición de Hecho

## 📦 Alcance Funcional

- [ ] El endpoint permite autenticar usuarios registrados.
- [ ] Las contraseñas son verificadas de forma cifrada.
- [ ] Se genera un token JWT válido y utilizable.
- [ ] Las respuestas JSON cumplen el contrato establecido.

  ## 🧪 Pruebas Completadas

- [ ] Se validaron las rutas `/api/login` con casos válidos y de error.
- [ ] Se verificó la validez del token JWT.
- [ ] Se confirmaron los códigos de estado HTTP (200, 401, 404).

  ## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Incluye ejemplos de éxito y error.
- [ ] Se detalla formato y duración del token.

  ## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 cuando faltan campos obligatorios.
- [ ] Se devuelve código HTTP 401 cuando la contraseña no coincide.
- [ ] Se devuelve código HTTP 404 cuando el usuario no existe.
- [ ] Se devuelve código HTTP 500 cuando ocurre un error inesperado en el servidor.
- [ ] El campo `mensaje` en el JSON incluye un texto amigable y claro para el usuario técnico o frontend.

