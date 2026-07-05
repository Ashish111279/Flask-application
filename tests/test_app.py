import json
import pytest
from app import app

@pytest.fixture(autouse=True)
def reset_data_file(tmp_path, monkeypatch):
    data_file = tmp_path / 'school_records.json'
    monkeypatch.setattr('app.DATA_FILE', str(data_file))
    initial = [
        {'id': 1, 'name': 'John Doe', 'grade': '10', 'section': 'A', 'marks': {'math': 90}},
        {'id': 2, 'name': 'Jane Smith', 'grade': '11', 'section': 'B', 'marks': {'math': 95}}
    ]
    data_file.write_text(json.dumps(initial))
    return str(data_file)

@pytest.fixture()
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()['message'] == 'School Records API'


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {'status': 'healthy'}


def test_list_records(client):
    response = client.get('/records')
    assert response.status_code == 200
    assert response.is_json
    assert len(response.get_json()) == 2


def test_get_record(client):
    response = client.get('/records/1')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()['name'] == 'John Doe'


def test_create_record(client):
    payload = {'name': 'New Student', 'grade': '12', 'section': 'C', 'marks': {'math': 88}}
    response = client.post('/records', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 3
    assert data['name'] == 'New Student'


def test_update_record(client):
    response = client.put('/records/1', json={'grade': '11', 'marks': {'math': 100}})
    assert response.status_code == 200
    data = response.get_json()
    assert data['grade'] == '11'
    assert data['marks']['math'] == 100


def test_delete_record(client):
    response = client.delete('/records/1')
    assert response.status_code == 200
    assert response.get_json() == {'deleted': 1}

    list_response = client.get('/records')
    assert len(list_response.get_json()) == 1
