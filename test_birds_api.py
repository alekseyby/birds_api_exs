import os
import tempfile
import pytest
import app as appl


@pytest.fixture
def client():
    db_fd, appl.app.config['DATABASE'] = tempfile.mkstemp()
    appl.app.config['TESTING'] = True
    client = appl.app.test_client()

    with appl.app.app_context():
        appl.init_db()

    yield client

    os.close(db_fd)
    os.unlink(appl.app.config['DATABASE'])


def test_api_bird_case0(client):
    """Request with no parameters."""
    rv = client.get('/birds')
    assert rv.status_code == 200

def test_api_add_bird_case1(client):
    """Valid bird."""
    rv = client.post('/birds', json={'species': 'pigeon', 'name': 'Perez', 'color': 'black & white',
                                   'body_length': 12, 'wingspan': 15})
    assert rv.status_code == 201, 'Valid bird'
    assert b'Database successfully updated' in rv.data


def test_api_birds_case2(client):
    """Request with attribute."""
    rv = client.get('/birds?attribute=color')
    assert rv.status_code == 200, 'Valid attribute'
    rv = client.get('/birds?attribute=qwerty')
    assert rv.status_code == 400, 'Invalid attribute'

def test_api_birds_case3(client):
    """Request with invalid attribute."""
    rv = client.get('/birds?attribute=invalid')
    assert rv.status_code == 400, 'Invalid attribute'
    assert b"Got unexpected value 'invalid' of 'attribute' parameter" in rv.data