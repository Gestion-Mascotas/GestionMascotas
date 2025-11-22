# app/services/mascota_service.py

from typing import Tuple

from sqlalchemy.orm import Session

from app.repository.mascota_repository import MascotaRepository
from app.domain.mascota_schema import MascotaUpdate, MascotaOut, MascotaCreate
from app.domain.usuario_schema import StandardResponse, ErrorDetail


class MascotaService:
    def __init__(self, db: Session):
        self.repo = MascotaRepository(db)

    # ---------- HU-003: Crear Mascota ----------
    def crear_mascota(
        self,
        usuario_id: int | None,
        datos_mascota: MascotaCreate
    ) -> Tuple[int, StandardResponse]:

        #Usuario no autenticado
        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para registrar una mascota.",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        # Validación de campos obligatorios
        errores: list[ErrorDetail] = []

        if not datos_mascota.nombre:
            errores.append(ErrorDetail(
                field="nombre",
                message="El campo nombre es obligatorio.",
            ))

        if not datos_mascota.especie:
            errores.append(ErrorDetail(
                field="especie",
                message="El campo especie es obligatorio.",
            ))

        #Campos obligatorios faltantes
        if errores:
            resp = StandardResponse(
                mensaje="Campos obligatorios faltantes.",
                success=False,
                error_code="400",
                details=errores,
                data=None,
            )
            return 400, resp

        # Validación de valores numéricos
        if datos_mascota.edad is not None and datos_mascota.edad < 0:
            errores.append(ErrorDetail(
                field="edad",
                message="El campo edad debe ser mayor o igual a 0",
            ))

        if datos_mascota.peso is not None and datos_mascota.peso < 0:
            errores.append(ErrorDetail(
                field="peso",
                message="El campo peso debe ser mayor o igual a 0",
            ))

        if errores:
            resp = StandardResponse(
                mensaje="Datos inválidos en la solicitud",
                success=False,
                error_code="400",
                details=errores,
                data=None,
            )
            return 400, resp

        #Duplicado de mascota
        mascota_existente = self.repo.obtener_por_nombre_y_usuario(
            nombre=datos_mascota.nombre,
            usuario_id=usuario_id,
        )

        if mascota_existente:
            resp = StandardResponse(
                mensaje="Ya existe una mascota registrada con ese nombre.",
                success=False,
                error_code="409",
                details=None,
                data=None,
            )
            return 409, resp

        #Registro exitoso
        try:
            mascota_nueva = self.repo.crear(
                usuario_id=usuario_id,
                datos=datos_mascota.model_dump()
            )

            mascota_out = MascotaOut(
                id=mascota_nueva.id,
                nombre=mascota_nueva.nombre,
                especie=mascota_nueva.especie,
                raza=mascota_nueva.raza,
                edad=mascota_nueva.edad,
                peso=mascota_nueva.peso,
                sexo=mascota_nueva.sexo,
                usuario_id=mascota_nueva.usuario_id,
            )

            resp = StandardResponse(
                mensaje="Mascota registrada exitosamente",
                success=True,
                error_code=None,
                details=None,
                data=mascota_out.model_dump()
                if hasattr(mascota_out, "model_dump")
                else mascota_out.model_dump(),
            )
            return 201, resp

        except Exception:
            resp = StandardResponse(
                mensaje="Error al crear la mascota",
                success=False,
                error_code="500",
                details=None,
                data=None,
            )
            return 500, resp


     # ---------- HU-004: Consultar Mascota ----------
    def consultar_mascota(
        self,
        mascota_id: int,
        usuario_id: int | None
    ) -> Tuple[int, StandardResponse]:

        # Usuario no autenticado
        if usuario_id is None:
            resp = StandardResponse(
                mensaje="Debe iniciar sesión para consultar la mascota.",
                success=False,
                error_code="401",
                details=None,
                data=None,
            )
            return 401, resp

        # Buscar mascota
        mascota = self.repo.obtener_por_id(mascota_id)

        # Mascota no existe
        if not mascota:
            resp = StandardResponse(
                mensaje="Mascota no encontrada",
                success=False,
                error_code="404",
                details=None,
                data=None,
            )
            return 404, resp

        # Mascota existe pero no pertenece al usuario
        if mascota.usuario_id != usuario_id:
            resp = StandardResponse(
                mensaje="Acceso no autorizado",
                success=False,
                error_code="403",
                details=None,
                data=None,
            )
            return 403, resp

        # Construcción del objeto de salida
        mascota_out = MascotaOut(
            id=mascota.id,
            nombre=mascota.nombre,
            especie=mascota.especie,
            raza=mascota.raza,
            edad=mascota.edad,
            peso=mascota.peso,
            sexo=mascota.sexo,
            usuario_id=mascota.usuario_id,
        )

        # OK
        resp = StandardResponse(
            mensaje="Mascota consultada correctamente",
            success=True,
            error_code=None,
            details=None,
            data=(
                mascota_out.model_dump()
                if hasattr(mascota_out, "model_dump")
                else mascota_out.model_dump()
            ),
        )
        return 200, resp

    # ---------- HU-005: Actualizar Mascota ----------
    def actualizar_mascota(
        self,
        mascota_id: int,
        usuario_id: int,
        datos_actualizacion: MascotaUpdate,
    ) -> Tuple[int, StandardResponse]:
        mascota = self.repo.obtener_por_id(mascota_id)

        # Mascota no existe
        if not mascota:
            resp = StandardResponse(
                mensaje="Mascota no encontrada o acceso no autorizado",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        # Mascota existe pero no es del usuario
        if mascota.usuario_id != usuario_id:
            resp = StandardResponse(
                mensaje="Acceso no autorizado",
                success=False,
                error_code=None,
                details=None,
                data=None,
            )
            return 403, resp

        # Validación de datos
        errores: list[ErrorDetail] = []
        cambios = (
            datos_actualizacion.model_dump(exclude_unset=True)
            if hasattr(datos_actualizacion, "model_dump")
            else datos_actualizacion.dict(exclude_unset=True)
        )

        if "edad" in cambios and cambios["edad"] is not None and cambios["edad"] < 0:
            errores.append(
                ErrorDetail(
                    field="edad",
                    message="El campo edad debe ser mayor o igual a 0",
                )
            )

        if "peso" in cambios and cambios["peso"] is not None and cambios["peso"] < 0:
            errores.append(
                ErrorDetail(
                    field="peso",
                    message="El campo peso debe ser mayor o igual a 0",
                )
            )

        if errores:
            resp = StandardResponse(
                mensaje="Datos inválidos en la solicitud",
                success=False,
                error_code="VALIDATION.FAILED",
                details=errores,
                data=None,
            )
            return 400, resp

        # Aplicar cambios solo a los campos enviados
        mascota_actualizada = self.repo.actualizar(mascota, cambios)

        mascota_out = MascotaOut(
            id=mascota_actualizada.id,
            nombre=mascota_actualizada.nombre,
            especie=mascota_actualizada.especie,
            raza=mascota_actualizada.raza,
            edad=mascota_actualizada.edad,
            peso=mascota_actualizada.peso,
            sexo=mascota_actualizada.sexo,
            usuario_id=mascota_actualizada.usuario_id,
        )

        resp = StandardResponse(
            mensaje="Mascota actualizada correctamente",
            success=True,
            data=mascota_out.model_dump()
            if hasattr(mascota_out, "model_dump")
            else mascota_out.dict(),
            error_code=None,
            details=None,
        )
        return 200, resp

    # ---------- HU-006: Eliminar Mascota ----------
    def eliminar_mascota(
        self,
        mascota_id: int,
        usuario_id: int,
    ) -> Tuple[int, StandardResponse]:
        from app.models.mascota import Mascota  # evitar import circular

        mascota = self.repo.obtener_por_id(mascota_id)

        # Mascota no existe
        if not mascota:
            resp = StandardResponse(
                mensaje="Mascota no encontrada o acceso no autorizado",
                success=False,
                error_code="RESOURCE.NOT_FOUND",
                details=None,
                data=None,
            )
            return 404, resp

        # Mascota existe pero no pertenece al usuario
        if mascota.usuario_id != usuario_id:
            resp = StandardResponse(
                mensaje="Acceso no autorizado",
                success=False,
                error_code=None,
                details=None,
                data=None,
            )
            return 403, resp

        # Intentar eliminar
        try:
            self.repo.eliminar(mascota)
            resp = StandardResponse(
                mensaje="Mascota eliminada exitosamente",
                success=True,
                data=None,
                error_code=None,
                details=None,
            )
            return 200, resp
        except Exception:
            resp = StandardResponse(
                mensaje="Error al eliminar la mascota",
                success=False,
                data=None,
                error_code=None,
                details=None,
            )
            return 500, resp
