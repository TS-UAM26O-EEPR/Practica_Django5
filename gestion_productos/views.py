from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from gestion_productos.DAO.productoDAO import ProductoDAO
from gestion_productos.exceptions.productoExceptions import (
    ConflictoProducto_409,
    DatosInvalidos_400,
    ErrorInternoServidor_500,
    ProductoNoAutorizado_401,
    ProductoNoEncontrado_404,
    ProductoProhibido_403,
)
from .serializers import ProductoCompletoSerializer, ProductoParcialSerializer


class ProductoViewSet(viewsets.ViewSet):
    """API para la gestión de Productos."""

    @swagger_auto_schema(
        operation_summary="Obtener todos los productos",
        responses={
            200: "Éxito",
            401: "No autorizado",
            403: "Prohibido",
            500: "Error interno del servidor",
        },
    )
    def list(self, request, *args, **kwargs):
        """Devuelve una lista de todos los productos."""
        try:
            productos = ProductoDAO.obtener_todos()
            serializer = ProductoCompletoSerializer(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductoNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ProductoProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Obtener un producto por ID",
        responses={
            200: "Éxito",
            401: "No Autorizado",
            403: "Prohibido",
            404: "Producto no encontrado",
            500: "Error interno del servidor",
        },
    )
    def retrieve(self, request, pk=None):
        """Obtiene los detalles de un producto específico utilizando su ID."""
        try:
            producto = ProductoDAO.obtener_producto_por_id(pk)
            serializer = ProductoCompletoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductoNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ProductoProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Crear un nuevo producto",
        request_body=ProductoCompletoSerializer,
        responses={
            201: "Producto creado exitosamente",
            400: "Error en la validación",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def create(self, request):
        """Crea un nuevo producto con la información proporcionada."""
        try:
            producto = ProductoDAO.crear_producto(**request.data)
            return Response(
                ProductoCompletoSerializer(producto).data,
                status=status.HTTP_201_CREATED,
            )
        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Actualizar un producto (completo)",
        request_body=ProductoCompletoSerializer,
        responses={
            200: "Producto actualizado exitosamente",
            400: "Datos inválidos",
            404: "Producto no encontrado",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def update(self, request, pk=None):
        """Actualiza completamente un producto especificado por su ID."""
        try:
            usuarioDTO = ProductoDAO.actualizar_producto(pk, **request.data)
            return Response(
                ProductoCompletoSerializer(usuarioDTO).data,
                status=status.HTTP_200_OK,
            )
        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Actualizar un producto (parcialmente)",
        request_body=ProductoParcialSerializer,
        responses={
            200: "Producto actualizado parcialmente",
            400: "Datos inválidos",
            404: "Producto no encontrado",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un producto especificado por su ID."""
        try:
            productoDTO = ProductoDAO.actualizar_producto_parcial(pk, **request.data)
            return Response(
                ProductoParcialSerializer(productoDTO).data,
                status=status.HTTP_200_OK,
            )
        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except ErrorInternoServidor_500 as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Elimina un producto (borrado lógico).",
        responses={
            200: "Producto eliminado correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Producto no encontrado",
        },
    )
    def destroy(self, request, pk=None):
        """Marca el producto como eliminado sin borrarlo físicamente."""
        try:
            ProductoDAO.eliminar_producto(pk)
            return Response(
                {"mensaje": "Producto eliminado correctamente"},
                status=status.HTTP_200_OK,
            )
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Restaurar un producto eliminado.",
        responses={
            200: "Producto restaurado exitosamente",
            401: "No autorizado",
            400: "El producto no estaba eliminado",
            404: "Producto no encontrado",
        },
    )
    def restore(self, request, pk=None):
        """Restaura un producto que había sido marcado como eliminado lógicamente."""
        try:
            ProductoDAO.restaurar_producto(pk)
            return Response(
                {"mensaje": "Producto restaurado correctamente"},
                status=status.HTTP_200_OK,
            )
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="search")
    @swagger_auto_schema(
        operation_summary="Buscar productos por nombre o descripción",
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Texto a buscar en nombre o descripción",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: ProductoCompletoSerializer(many=True),
            400: "Consulta de búsqueda inválida",
            401: "No autorizado",
            403: "Prohibido",
            404: "No se encontraron productos",
            500: "Error interno del servidor",
        },
    )
    def search(self, request):
        query = request.GET.get("q", "")
        if not query:
            return Response(
                {"error": "Debe proporcionar un parámetro de búsqueda"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        productos = ProductoDAO.buscar_productos(query)
        serializer = ProductoCompletoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="filtrar-precio")
    @swagger_auto_schema(
        operation_summary="Filtrar productos por rango de precio",
        manual_parameters=[
            openapi.Parameter(
                "precio_min",
                openapi.IN_QUERY,
                description="Precio mínimo",
                type=openapi.TYPE_NUMBER,
                required=True,
            ),
            openapi.Parameter(
                "precio_max",
                openapi.IN_QUERY,
                description="Precio máximo",
                type=openapi.TYPE_NUMBER,
                required=True,
            ),
        ],
        responses={
            200: "Éxito",
            400: "Parámetros inválidos",
            500: "Error interno del servidor",
        },
    )
    def filtrar_por_precio(self, request):
        """Filtra productos por rango de precio."""
        try:
            precio_min = request.query_params.get("precio_min")
            precio_max = request.query_params.get("precio_max")

            if precio_min is None or precio_max is None:
                return Response(
                    {"error": "Debe proporcionar precio_min y precio_max"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            productos = ProductoDAO.filtrar_por_rango_precio(
                precio_min,
                precio_max,
            )
            serializer = ProductoCompletoSerializer(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (ValueError, TypeError, ValidationError) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Actualizar imagen de producto",
        manual_parameters=[
            openapi.Parameter(
                "image_link",
                openapi.IN_QUERY,
                description="string (URL válida, máximo 200 caracteres)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: "Imagen actualizada exitosamente",
            400: "URL inválida o excede el límite de caracteres",
            404: "Producto no encontrado",
            500: "Error interno del servidor",
        },
    )
    def update_image(self, request, pk=None):
        """Actualiza la URL de la imagen de un producto específico."""
        try:
            img = request.GET.get("image_link", "")
            producto = ProductoDAO.actualizar_img(pk, img)
            data = {
                "codigo": 200,
                "mensaje": "Imagen del producto actualizada exitosamente.",
                "resultado": {
                    "id": str(producto.id),
                    "image_link": producto.image_link,
                    "modified_at": producto.modified_at.isoformat(),
                },
            }
            return Response(data, status=status.HTTP_200_OK)
        except ProductoNoEncontrado_404:
            data = {
                "codigo": 404,
                "mensaje": "Producto no encontrado.",
                "resultado": "null",
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            data = {
                "codigo": 400,
                "mensaje": "La URL de la imagen no es válida o excede el límite de caracteres.",
                "resultado": "null",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Desactivar un producto",
        responses={
            200: "Producto desactivado exitosamente",
            401: "No autorizado",
            400: "El producto ya estaba desactivado",
            403: "Prohibido",
            404: "Producto no encontrado",
            500: "Error interno del servidor",
        },
    )
    def deactivate(self, request, pk=None):
        """Desactiva un producto estableciendo el campo status en false."""
        try:
            producto = ProductoDAO.desactivar_producto(pk)
            data = {
                "codigo": 200,
                "mensaje": "Producto desactivado exitosamente.",
                "resultado": {
                    "id": str(producto.id),
                    "status": producto.status,
                    "modified_at": producto.modified_at.isoformat(),
                },
            }
            return Response(data, status=status.HTTP_200_OK)
        except ProductoNoEncontrado_404 as e:
            return Response(
                {"codigo": 404, "mensaje": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response(
                {"codigo": 400, "mensaje": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Activar un producto",
        responses={
            200: "Producto restaurado exitosamente",
            401: "No autorizado",
            400: "El producto ya estaba activado",
            404: "Producto no encontrado",
        },
    )
    def activate(self, request, pk=None):
        """Activa un producto estableciendo el campo status en true."""
        try:
            ProductoDAO.activar_producto(pk)
            return Response(
                {"mensaje": "Producto activado correctamente"},
                status=status.HTTP_200_OK,
            )
        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
