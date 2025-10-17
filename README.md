# Proyecto ETL - Productos de FakeStore API

Un pipeline ETL (Extract, Transform, Load) desarrollado en Python que extrae datos de productos desde la FakeStore API, los transforma usando Apache Spark y los carga en una base de datos PostgreSQL.

## 📋 Descripción

Este proyecto implementa un pipeline ETL completo que:

1. **Extrae** datos de productos desde la [FakeStore API](https://fakestoreapi.com/products)
2. **Transforma** los datos usando Apache Spark para limpiarlos y estructurarlos
3. **Carga** los datos procesados en una base de datos PostgreSQL
4. **Genera** un reporte de productos por categoría

## 🏗️ Arquitectura del Proyecto

Se opta por un enfoque modular para una mejor organización de los elementos del proyecto tanto para las 
etapas de ETL como de las configuraciones de bases de datos, sesión en spark y el manejo de excepciones.

```
ETL/
├── main.py                 # Archivo principal del pipeline ETL
├── requirements.txt        # Dependencias de Python
├── config/
│   ├── config.ini         # Configuración de la base de datos
│   └── postgresql-42.7.8.jar  # Driver JDBC de PostgreSQL
├── core/
│   └── exceptions.py      # Excepciones personalizadas
├── etl/
│   ├── extract.py         # Módulo de extracción de datos
│   ├── transform.py       # Módulo de transformación con Spark
│   └── load.py           # Módulo de carga a PostgreSQL
└── utils/
    └── spark_session.py   # Configuración de sesión de Spark
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Apache Spark (PySpark)** - Para procesamiento de datos
- **PostgreSQL** - Base de datos de destino
- **Requests** - Para consumo de API REST
- **ConfigParser** - Para gestión de configuración

## 📦 Requisitos

### Dependencias de Python
```bash
pyspark
requests
configparser
psycopg2-binary
```

### Requisitos del Sistema
- Python 3.11 o superior
- Java 8+ (requerido por Spark)
- PostgreSQL
- Acceso a internet (para consumir la API)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd Projects
```

### 2. Crear entorno virtual
```bash
python -m venv env
source env/bin/activate  # En macOS/Linux
# o
env\Scripts\activate     # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r ETL/requirements.txt
```

### 4. Configurar PostgreSQL

Crea una base de datos PostgreSQL y ajusta la configuración en `ETL/config/config.ini`:

```ini
[postgres]
user = user
password = password
host = localhost
port = 5432
database = tu_base_de_datos
jdbc_driver_path = config/postgresql-42.7.8.jar
```

### 5. Plantilla de configuración (opcional)
Si se planea mantener una configuración privada, puedes usar `config.ini.template` como base.

## ▶️ Ejecución

Para ejecutar el pipeline ETL completo:

```bash
cd ETL
python main.py
```

## 📊 Funcionalidades

### Extracción
- Consume la FakeStore API para obtener datos de productos
- Manejo de errores de conexión y respuesta
- Validación de códigos de estado HTTP

### Transformación
- Limpieza y tipado de datos
- Estructuración de datos anidados (ratings)
- Creación de DataFrame de Spark con esquema definido
- Generación de reporte agregado por categoría

### Carga
- Inserción de datos en PostgreSQL usando JDBC
- Creación de dos tablas:
  - `productos`: Datos principales de productos
  - `reporte_productos_por_categoria`: Reporte agregado

## 🔧 Estructura de Datos

### Esquema de Productos
```python
- id (Long): Identificador único del producto
- title (String): Nombre del producto
- price (Double): Precio del producto
- description (String): Descripción del producto
- category (String): Categoría del producto
- image (String): URL de la imagen
- rating_rate (Double): Calificación promedio
- rating_count (Long): Número de calificaciones
```

## 🚨 Manejo de Errores

El proyecto incluye excepciones personalizadas para el manejo de errores en cada etapa del ETL:

- `ExtractError`: Errores durante la extracción de datos
- `TransformError`: Errores durante la transformación
- `LoadError`: Errores durante la carga de datos

## 📈 Monitoreo y Logs

- Logs detallados en cada etapa del proceso
- Visualización de datos usando `show()` de Spark
- Información de éxito/error al finalizar el proceso

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request


## 🔄 Versiones

- **v1.0.0** - Versión inicial con funcionalidad ETL completa
