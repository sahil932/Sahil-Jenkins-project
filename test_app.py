import pytest
import importlib
module = importlib.import_module("Sahil.Bhuva")
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