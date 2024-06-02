import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_short_url(client):
    rv = client.post('/', data={'long_url': 'http://example.com'})
    assert b'Short URL:' in rv.data
