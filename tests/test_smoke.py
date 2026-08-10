import os

os.environ.setdefault('SECRET_KEY', 'ci-test-secret')
os.environ.setdefault('DATABASE_URI', 'sqlite:///ci-test.db')

from app import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_homepage_loads():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
