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

def test_cards_get_list():
    # Needs refactoring to make sure user and card with id's '1' are created before this is run
    for card in Card.query.all():
        db.session.delete(card)
        db.session.commit()

    for user in User.query.all():
        db.session.delete(user)
        db.session.commit()

    user = User(username='coolguy123', email='coolguy123@gmail.com')
    fe_card1 = Card(category='technicalFE', front='an FE question', rating=5.0)
    fe_card2 = Card(category='technicalFE', front='an FE question', rating=4.0)
    be_card1 = Card(category='technicalBE', front='a BE question', rating=5.0)
    be_card2 = Card(category='technicalBE', front='a BE question', rating=3.0)
    behav_card1 = Card(category='behavioral', front='a behavioral question', rating=4.0)
    behav_card2 = Card(category='behavioral', front='a behavioral question', rating=3.0)
    cards = [fe_card1, fe_card2, be_card1, be_card2, behav_card1, behav_card2]
    for card in cards:
        user.cards.append(card)

    db.session.add(user)
    db.session.commit()

    response = app.test_client().get('api/v1/users/1/cards')
    json_data = json.loads(response.data)['data']

    assert response.status_code == 200

    assert type(json_data['BEtechnicalCards']) == list
    for card in json_data['BEtechnicalCards']:
        assert type(card['id']) == str
        assert card['type'] == 'flashCard'
        assert card['attributes']['category'] == 'technicalBE'
        assert type(card['attributes']['competenceRating']) == float or int
        assert type(card['attributes']['frontSide']) == str
        assert type(card['attributes']['backSide']) == str
        assert type(card['attributes']['userId']) == str

    assert type(json_data['FEtechnicalCards']) == list
    for card in json_data['FEtechnicalCards']:
        assert type(card['id']) == str
        assert card['type'] == 'flashCard'
        assert card['attributes']['category'] == 'technicalFE'
        assert type(card['attributes']['competenceRating']) == float or int
        assert type(card['attributes']['frontSide']) == str
        assert type(card['attributes']['backSide']) == str
        assert type(card['attributes']['userId']) == str

    assert type(json_data['behavioralCards']) == list
    for card in json_data['behavioralCards']:
        assert type(card['id']) == str
        assert card['type'] == 'flashCard'
        assert card['attributes']['category'] == 'behavioral'
        assert type(card['attributes']['competenceRating']) == float or int
        assert type(card['attributes']['frontSide']) == str
        assert type(card['attributes']['backSide']) == str
        assert type(card['attributes']['userId']) == str
