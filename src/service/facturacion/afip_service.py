from pyafipws.wsaa import WSAA
from injector import inject

class AFIPService:
    @inject
    def __init__(self, cuit: str, cert_path: str, key_path: str, wsaa: WSAA):
        self.cuit = cuit
        self.cert_path = cert_path
        self.key_path = key_path
        self.wsaa = wsaa

    def obtener_token(self):
        # Autenticar y obtener el token usando argumentos posicionales en el orden correcto
        return self.wsaa.Autenticar("wsfe", self.cert_path, self.key_path)
