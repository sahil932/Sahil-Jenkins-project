import pytest
import sys
import importlib.util

# Load the app file directly by path (handles dot in filename)
spec = importlib.util.spec_from_file_location("app", "Sahil.Bhuva.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_vote_france(client):
    response = client.post('/vote', data={'choice': 'A'})
    assert response.status_code == 302

def test_vote_argentina(client):
    response = client.post('/vote', data={'choice': 'B'})
    assert response.status_code == 302

def test_reset(client):
    response = client.get('/reset')
    assert response.status_code == 302