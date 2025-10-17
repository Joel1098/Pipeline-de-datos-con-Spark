from core.exceptions import LoadError


def load_to_postgres(df, db_properties, table_name):
    
    print("Cargando datos a PostgreSQL...")
    
    try:
        df.write.jdbc(
            url= db_properties['url'],
            table = table_name,
            mode = 'overwrite',  # Cambia a 'append' si deseas agregar datos en lugar de sobrescribir
            properties = db_properties['properties']
        )
        print(f"Carga de datos a la tabla '{table_name}' exitosa.")
    except Exception as e:
        raise LoadError("Error al cargar datos a PostgreSQL.", original_exception=e)
        