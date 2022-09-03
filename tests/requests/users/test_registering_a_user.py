from app import app, db
from models.user import User 
from models.card import Card
import json

def test_register_user():
    body = {'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com'}

    response = app.test_client().post(
            'api/v1/users',
            data=json.dumps(body),
            headers={"Content-Type": "application/json"}
        )

    json_data = json.loads(response.data)['data']

    assert response.status_code == 201

    assert json_data['type'] == 'users'
    assert json_data['attributes']['username'] == 'bonnyjowman08'
