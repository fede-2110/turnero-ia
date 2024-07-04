import unittest
import os

class TestFileAccess(unittest.TestCase):

    def setUp(self):
        # Configurar las rutas de los archivos
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.cert_path = os.path.join(base_dir, 'certs', 'cert.cert')
        self.key_path = os.path.join(base_dir, 'certs', 'private.key')

    def test_cert_file_exists(self):
        print(f"Verificando existencia del archivo: {self.cert_path}")
        self.assertTrue(os.path.exists(self.cert_path), f"El archivo {self.cert_path} no existe")

    def test_key_file_exists(self):
        print(f"Verificando existencia del archivo: {self.key_path}")
        self.assertTrue(os.path.exists(self.key_path), f"El archivo {self.key_path} no existe")

    def test_cert_file_readable(self):
        print(f"Verificando permisos de lectura del archivo: {self.cert_path}")
        self.assertTrue(os.access(self.cert_path, os.R_OK), f"No se puede leer el archivo {self.cert_path}")

    def test_key_file_readable(self):
        print(f"Verificando permisos de lectura del archivo: {self.key_path}")
        self.assertTrue(os.access(self.key_path, os.R_OK), f"No se puede leer el archivo {self.key_path}")

if __name__ == '__main__':
    unittest.main()
