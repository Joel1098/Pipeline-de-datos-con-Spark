from pyspark.sql import SparkSession


def get_spark_session(app_name, driver_path):
    """
    Create and return a Spark session with the specified application name and JDBC driver path.

    Parameters:
    app_name (str): The name of the Spark application.
    driver_path (str): The path to the JDBC driver.

    Returns:
    SparkSession: A configured Spark session.
    """
    spark = (SparkSession.builder
             .appName(app_name)
             .master("local[*]")
             .config("spark.driver.extraClassPath", driver_path)
             .getOrCreate())
    return spark

