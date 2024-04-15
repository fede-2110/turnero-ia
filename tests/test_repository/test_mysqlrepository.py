import pytest
import pymysql
from src.repository.mysql_repository import MysqlRepository
from app import create_app

@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app

def test_my_sql_connection():
    host = "localhost"  
    port = 3307  
    user = "root"  
    password = "admin"  
    db = "turneroai"

    try:
        # Intentar establecer una conexión
        connection = pymysql.connect(host=host, user=user, port=port, password=password, db=db)
        assert connection.open
        connection.close()
    except pymysql.MySQLError as e:
        pytest.fail(f"Error al conectar a MySQL: {e}")
        