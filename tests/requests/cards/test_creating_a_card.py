from app import app, db
from models.user import User
from models.card import Card
import json

def test_card_create():
    body = {'category': 'technicalBE', 'frontSide': 'What is MVC?', 'backSide': 'stuff and things'}
    response = app.test_client().post(
        'api/v1/users/1/cards',
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
        )
    json_data = json.loads(response.data)['data']

    assert response.status_code == 201

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert type(json_data['attributes']['competenceRating']) == float or int
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'stuff and things'

def test_card_create_invalid_user_id():
    response = app.test_client().post('api/v1/users/1000/cards', data={'category': 'technicalBE', 'frontSide': 'What is MVC?', 'backSide': 'stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'invalid user id'
