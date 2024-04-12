# app/error_handlers.py
from src.utils.api_response import ApiResponse

def register_error_handlers(app):

    @app.errorhandler(500)
    def handle_500_error(error):
        return ApiResponse.server_error("Ocurrio un error interno en el servidor", 500)

    @app.errorhandler(403)
    def forbidden(error):
        return ApiResponse.failure(("No tienes permiso para acceder a este recurso."), 403)