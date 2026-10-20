# API REST - Módulo de Gestión de Productos

Backend desarrollado con **Django 4** y **Django REST Framework (DRF)** para la administración de productos, integrado con **PostgreSQL** mediante Docker.

---

## Cambios e Implementaciones en esta Versión

En esta fase del proyecto se añadió e integró el módulo completo de `gestion_productos`:

* **Estructura Arquitectónica (DAO):** Implementación del patrón Data Access Object (DAO) y excepciones personalizadas para desacoplar la lógica de acceso a datos.
* **Modelo y Serializadores:** Creación del modelo `Producto` junto a sus serializadores en DRF para manejo y validación de datos JSON.
* **Vistas y Rutas:** Configuración de endpoints para operaciones CRUD de productos e integración en `urls.py` principal.
* **Configuración del Proyecto:** Registro del módulo `gestion_productos` e integración de librerías de filtrado (`django-filter`) y soporte CORS (`django-cors-headers`).
* **Documentación Interactiva:** Exposición de endpoints y esquemas mediante Swagger UI (`drf-yasg`).

---

## Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Framework:** Django 4.x / Django REST Framework
* **Base de Datos:** PostgreSQL (en contenedor Docker)
* **Documentación:** Swagger / OpenAPI (`drf-yasg`)
* **Herramientas:** Docker Compose, VS Code, Git
