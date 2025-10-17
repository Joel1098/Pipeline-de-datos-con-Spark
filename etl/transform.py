from core.exceptions import TransformError
from pyspark.sql.functions import col
from pyspark.sql.types import (DecimalType, DoubleType, LongType, StringType,
                               StructField, StructType)


def transform_products(spark, raw_data):
    
    """
    Transforma los datos crudos en los productos de Spark con el esquema definido.
    """
    
    print("Transformando datos...")
    try:
        schema = StructType([
            StructField("id", LongType(), True),
            StructField("title", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("description", StringType(), True),
            StructField("category", StringType(), True),
            StructField("image", StringType(), True),
            StructField("rating", StructType([
                StructField("rate", DoubleType(), True),
                StructField("count", LongType(), True)
            ]), True)
        ])
        
        df = spark.createDataFrame(raw_data, schema)
        
        # 3. Transformación principal: limpiar, aplanar y seleccionar columnas.
        # - Aplanamos la estructura anidada de 'rating' para crear 'puntuacion' y 'cantidad_votos'.
        # - Eliminamos columnas que no usaremos en la base de datos ('rating', 'image', 'description').
        # - Seleccionamos y renombramos las columnas finales para mayor claridad.
        
        df_cleaned = df.withColumn("puntuacion", col("rating.rate")) \
                    .withColumn("cantidad_votos", col("rating.count")) \
                        .drop("rating", "image", "description") \
                            .select(
                                col("id").alias("producto_id"),
                                col("title").alias("nombre"),
                                col("price").cast(DecimalType(10, 2)).alias("precio"),
                                col("category").alias("categoria"),
                                col("puntuacion"),
                                col("cantidad_votos")
                            )
                            
        # 4. Transformación secundaria: crear un reporte agregado.
        # - Agrupamos por 'categoria'.
        # - Contamos el número de productos en cada grupo.
        # - Renombramos la columna 'count' para que sea más descriptiva.
        # - Ordenamos el resultado para ver las categorías con más productos primero.
        df_report = df_cleaned.groupBy("categoria").count().withColumnRenamed("count", "numero_de_productos")\
            .orderBy(col("numero_de_productos").desc())
            
        print("Transformación de datos exitosa.")
        return df_cleaned, df_report
        
    except Exception as e:
        raise TransformError("Error al transformar los datos.",
        original_exception=e
        )
    