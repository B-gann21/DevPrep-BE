from app import app, db
from models.user import User
from models.card import Card
import json

def test_card_update():
    cards = Card.query.all()
    for card in cards:
        db.session.delete(card)
        db.session.commit()

    card = Card(
        category="technicalBE",
        front="Do ya like apples?",
        user_id=1
    )
    db.session.add(card)
    db.session.commit()

    body = {'backSide': 'updated stuff and things'}
    response = app.test_client().patch(
        f"api/v1/users/1/cards/{card.id}",
        data=json.dumps(body),
        headers={"Content-Type": "application/json"}
        )
    json_data = json.loads(response.data)['data']

    assert response.status_code == 200

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert json_data['attributes']['frontSide'] == 'Do ya like apples?'
    assert json_data['attributes']['backSide'] == 'updated stuff and things'

def test_card_update_invalid_user_id():
    response = app.test_client().patch('api/v1/users/1000/cards/1', data={'backSide': 'updated stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'invalid user id'
