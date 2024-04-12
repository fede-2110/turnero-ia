from flask import jsonify, Response
import json

class ApiResponse:
    @staticmethod
    def success(data=None, message="Operación exitosa", status=200, meta=None):
        response_content = {"success": True, "message": message, "data": data}
        if meta:
            response_content['meta'] = meta
        response_data = json.dumps(response_content)
        return Response(response_data, status=status, mimetype='application/json')
        
    @staticmethod
    def redirection(message="Redirección", status=300):
        response_data = json.dumps({"success": True, "message": message})
        return Response(response_data, status=status, mimetype='application/json')

    @staticmethod
    def client_error(message="Error en la solicitud", status=400):
        response_data = json.dumps({"success": False, "message": message})
        return Response(response_data, status=status, mimetype='application/json')

    @staticmethod
    def server_error(message="Error interno del servidor", status=500):
        response_data = json.dumps({"success": False, "message": message})
        return Response(response_data, status=status, mimetype='application/json')
    
    @staticmethod
    def failure(message="Operación fallida", status=400):
        response_data = json.dumps({"success": False, "message": message})
        return Response(response_data, status=status, mimetype='application/json')