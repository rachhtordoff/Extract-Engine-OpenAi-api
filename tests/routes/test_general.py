from flask import json
from src import app
import pytest


# create client fixture
@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_health_route(client):
    response = client.get('/health')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'OK'
    assert data['message'] == 'Service is up and running'


def test_health_route_wrong_method(client):
    response = client.post('/health')
    assert response.status_code == 405
