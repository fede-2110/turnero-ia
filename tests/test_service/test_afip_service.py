import unittest
from src.service.facturacion.afip_service import AFIPService
import os
from pyafipws.wsaa import WSAA

class TestAFIPService(unittest.TestCase):

    def test_obtener_token_real(self):
        # Arrange
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cert_path = os.path.join(base_dir, 'certs', 'cert.cert')
        key_path = os.path.join(base_dir, 'certs', 'private.key')
        cuit = '27360866403'
        
        # Imprimir la ruta para verificación
        print(f"Ruta del certificado: {cert_path}")
        print(f"Ruta de la clave: {key_path}")
        
        # Act
        afip_service = AFIPService(cuit, cert_path, key_path, WSAA())
        token = afip_service.obtener_token()

        # Assert
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        print("Token obtenido:", token)
        
if __name__ == '__main__':
    unittest.main()