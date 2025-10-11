# '[HU-004] Consulta de Mascota'

## 📖 Historia de Usuario

Como usuario registrado 
Quiero consultar la información de una mascota
Para visualizar sus datos generales y mantener el seguimiento actualizado


## 🔁 Flujo Esperado

- El usuario accede al módulo de **consulta de mascotas**.  
- El sistema consume el endpoint `/api/mascotas/{id}`.  
- El backend valida que la mascota exista y pertenezca al usuario autenticado. 
- Se recuperan los datos generales de la mascota desde la base de datos.  
- El sistema devuelve la información en formato JSON estructurado. 


## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint **GET** `/api/mascotas/{id}`.  
- [ ] Se valida que el `id` exista en la base de datos. 
- [ ] Se verifica que el usuario autenticado tenga permiso de acceso. 
- [ ] Se retorna la información general de la mascota.  

### 2. 📆 Estructura de la información

- [ ] Respuesta exitosa:

```json
{
  "mensaje": "Consulta de mascota exitosa",
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

- [ ] Si la mascota no existe o no pertenece al usuario:

```json
{
  "mensaje": "Mascota no encontrada o acceso no autorizado",
  "error_code": "RESOURCE.NOT_FOUND",
  "success": false
}
```
- [ ] Si ocurre un error interno:

```json
{
  "mensaje": "Error al consultar la información de la mascota",
  "success": false
}
```


## 🔧 Notas Técnicas

## 🚀 Endpoint – Registro de Mascota

- **Método HTTP:** `GET`  
- **Ruta:** `/api/mascotas/{id}`  


## 📤 Ejemplo de Respuesta JSON

```json
{
  "mensaje": "Consulta de mascota exitosa",
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


## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Consulta exitosa

- **Precondición:** La mascota existe y pertenece al usuario.
- **Acción:** Enviar solicitud GET con el ID válido y token de autenticación.
- **Resultado esperado:**  
  - Código HTTP `200 OK`  
  - `success = true`  
  - Mensaje: “Consulta de mascota exitosa”  

### ❌ Caso 2: Mascota inexistente

- **Precondición:** El ID no corresponde a ninguna mascota registrada. 
- **Acción:** Ejecutar el endpoint con un ID inexistente.
- **Resultado esperado:**  
  - Código HTTP `404 Not Found`  
  - Mensaje: “Mascota no encontrada o acceso no autorizado.”  

### ❌ Caso 3: Usuario sin permisos

- **Precondición:** El usuario intenta consultar una mascota de otro usuario.  
- **Acción:** Enviar solicitud con token válido, pero sin permisos.
- **Resultado esperado:**  
  - Código HTTP `403 Forbidden`  
  - Mensaje: “Acceso no autorizado.”  

### ❌ Caso 4: Sin autenticación

- **Precondición:** No se envía token de autenticación.  
- **Acción:** Ejecutar GET sin encabezado `Authorization`.  
- **Resultado esperado:**  
  - Código HTTP `401 Unauthorized`  
  - Mensaje: “Debe iniciar sesión para consultar la información.”  

## ✅ Definición de Hecho

## 📦 Alcance Funcional

- [ ] El endpoint permite consultar mascotas registradas.
- [ ] Se valida la propiedad del recurso antes de mostrar los datos.
- [ ] El endpoint requiere autenticación. 

## 🧪 Pruebas Completadas

- [ ] Se probaron registros exitosos y fallas de acceso.  
- [ ] Se cubrieron los códigos 200, 401, 403 y 404. 
- [ ] Las pruebas unitarias y funcionales pasaron correctamente.  

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.  
- [ ] Se describen parámetros, estructura de respuesta y códigos de error.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 401 si el usuario no está autenticado.
- [ ] Se devuelve código HTTP 403 si intenta acceder a una mascota ajena.  
- [ ] Se devuelve código HTTP 404 si la mascota no existe.  
- [ ] Se devuelve código HTTP 500 ante errores del servidor.
- [ ] El campo `mensaje` comunica de forma clara el resultado al frontend.
