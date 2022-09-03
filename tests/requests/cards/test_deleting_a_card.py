from app import app, db
from models.user import User
from models.card import Card
import json

def test_card_delete():
    response = app.test_client().delete('api/v1/users/1/cards/1')

    assert response.status_code == 204

    response = app.test_client().delete('api/v1/users/1000/cards/1')
    json_data = json.loads(response.data)

    assert response.status_code == 400
    assert json_data['error'] == 'invalid card or user'

    response = app.test_client().delete('api/v1/users/1/cards/1000')
    json_data = json.loads(response.data)

    assert response.status_code == 400
    assert json_data['error'] == 'invalid card or user'
