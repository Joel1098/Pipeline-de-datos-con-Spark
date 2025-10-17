import configparser
import sys

from core.exceptions import ExtractError, LoadError, TransformError
from etl.extract import extract_products
from etl.load import load_to_postgres
from etl.transform import transform_products
from utils.spark_session import get_spark_session


def main():
    
    spark = None
    
    try:
        # -- Configuración --
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        df_config = config['postgres']
        db_properties = {
            "url": f"jdbc:postgresql://{df_config['host']}:{df_config['port']}/{df_config['database']}",
            "properties" : {
                "user": df_config['user'],
                "password": df_config['password'],
                "driver": "org.postgresql.Driver"
                    
                }   
        }
        
        API_URL = "https://fakestoreapi.com/products"
        
        
        
        spark = get_spark_session("ETL con API", df_config['jdbc_driver_path'])
        raw_products_data = extract_products(API_URL)
        
        for product in raw_products_data:
            if 'price' in product and product['price'] is not None:
                product['price'] = float(product['price'])
        
            if 'rating' in product and isinstance(product['rating'], dict) and 'rate' in product['rating']:
                    if product['rating']['rate'] is not None:
                        product['rating']['rate'] = float(product['rating']['rate'])
        df_products, df_report = transform_products(spark, raw_products_data)
        
        
                
        if df_products:
            df_products.show(5)
            load_to_postgres(df_products, db_properties, "productos")
        
        if df_report:
            df_report.show()
            load_to_postgres(df_report, db_properties, "reporte_productos_por_categoria")
        
        print("ETL finalizado con éxito.")
        
    except ExtractError as e:
        print(f"Error en la extracción: {e}")
        if e.original_exception:
            print(f"Excepción original: {e.original_exception}")
        sys.exit(1)
    except TransformError as e:
        print(f"Error en la transformación: {e}")
        if e.original_exception:
            print(f"Excepción original: {e.original_exception}")
        sys.exit(1)
    except LoadError as e:
        print(f"Error en la carga: {e}")
        if e.original_exception:
            print(f"Excepción original: {e.original_exception}")
        sys.exit(1)
    
    finally:
        if spark:
            print("\n⚙️  Deteniendo la sesión de Spark.")
            spark.stop()
            
if __name__ == "__main__":
    main()