# core/exceptions.py

class ETLBaseError(Exception):
    """Clase base para las excepciones personalizadas en este pipeline."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class ExtractError(ETLBaseError):
    """Excepción lanzada por errores en el proceso de extracción."""
    pass

class TransformError(ETLBaseError):
    """Excepción lanzada por errores en el proceso de transformación."""
    pass

class LoadError(ETLBaseError):
    """Excepción lanzada por errores en el proceso de carga a la base de datos."""
    pass