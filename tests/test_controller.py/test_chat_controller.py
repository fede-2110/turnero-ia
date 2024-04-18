import pytest
from app import create_app

@pytest.fixture(scope="module")
def app():
    app = create_app()
    return app

@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        yield app.test_client()

def test_real_chat_interaction(client):
        # Suponiendo que el endpoint '/chat/create' crea un nuevo thread
        response = client.post('/chat/create')
        assert response.status_code == 200
        thread_id = response.json['data']['thread_id']

        # Envía un mensaje real a través del endpoint '/chat/update/{thread_id}'
        response = client.post(f'/chat/update/{thread_id}', json={'message': 'Hola!'})
        assert response.status_code == 200
        assert len(response.json['data']['message']) > 0  # Verifica que la respuesta no esté vacía

