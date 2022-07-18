from app import app, db, User, Card
import json
# from models import UserModel, CardModel
db.create_all()

def test_register_user():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
        db.session.commit()

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

def test_login_user():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
        db.session.commit()

    body = {'username': 'bonnyjowman08', 'email': 'bonfjowman.hello@notreal.com'}
    seed_1 = User(email=body['email'], username=body['username'])
    seed_2 = User(email='test@test.com', username='megahacker3000')
    db.session.add(seed_1)
    db.session.add(seed_2)
    db.session.commit()
    response = app.test_client().post(
            'api/v1/login',
            data=json.dumps(body),
            headers={"Content-Type": "application/json"}
        )

    json_data = json.loads(response.data)['data']
    assert response.status_code == 200

    assert json_data['type'] == 'userDashboard'
    assert type(json_data['userId']) is str
    assert json_data['attributes']['username'] == 'bonnyjowman08'
    assert type(json_data['attributes']['preparednessRating']) is dict
    assert type(json_data['attributes']['preparednessRating']['technicalBE']) is float or "null"
    assert type(json_data['attributes']['preparednessRating']['technicalFE']) is float or "null"
    assert type(json_data['attributes']['preparednessRating']['behavioral']) is float or "null"
    assert type(json_data['attributes']['cwAttributes']) is dict
    assert type(json_data['attributes']['cwAttributes']['cwLeaderboardPosition']) is int or "null"
    assert type(json_data['attributes']['cwAttributes']['totalCompleted']) is int or "null"
    assert type(json_data['attributes']['cwAttributes']['languageRanks']) is dict

def test_update_user():
    body = {'username': 'bonnyjowman08', 'codewarsUsername': 'MichaelPutnam2'}
    user = User.query.filter_by(username='bonnyjowman08').first()

    response = app.test_client().patch(
            f'api/v1/users/{user.id}',
            data=json.dumps(body),
            headers={"Content-Type": "application/json"}
        )

    json_data = json.loads(response.data)['data']

    assert response.status_code == 200
    assert json_data['type'] == 'userDashboard'
    assert type(json_data['userId']) is str
    assert json_data['attributes']['username'] == 'bonnyjowman08'
    assert type(json_data['attributes']['preparednessRating']) is dict
    assert type(json_data['attributes']['preparednessRating']['technicalBE']) is float or "null"
    assert type(json_data['attributes']['preparednessRating']['technicalFE']) is float or "null"
    assert type(json_data['attributes']['preparednessRating']['behavioral']) is float or "null"
    assert type(json_data['attributes']['cwAttributes']) is dict
    assert type(json_data['attributes']['cwAttributes']['cwLeaderboardPosition']) is int or "null"
    assert type(json_data['attributes']['cwAttributes']['totalCompleted']) is int or "null"
    assert type(json_data['attributes']['cwAttributes']['languageRanks']) is dict

def xtest_update_user_invalid_username():
    body = {'username': 'bonnyjowman08', 'codewarsUsername': 'veryInvalidUsername5748576'}
    user = User.query.filter_by(username='bonnyjowman08').first()

    response = app.test_client().patch(
            f'api/v1/users/{user.id}',
            data=json.dumps(body),
            headers={"Content-Type": "application/json"}
        )

    json_data = json.loads(response.data)
    
    assert response.status_code == 404
    assert json_data['error'] == 'invalid codewars username'

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
    assert type(json_data['attributes']['competenceRating']) == float
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'stuff and things'

def test_card_create_invalid_user_id():
    response = app.test_client().post('api/v1/users/1000/cards', data={'category': 'technicalBE', 'frontSide': 'What is MVC?', 'backSide': 'stuff and things'})
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'invalid user id'

def xtest_card_get():
    # Needs refactoring to make sure user and card with id's '1' are created before this is run
    response = app.test_client().get('api/v1/users/1/cards/1')
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert json_data['type'] == 'flashCard'
    assert json_data['attributes']['category'] == 'technicalBE'
    assert type(json_data['attributes']['competenceRating']) == float
    assert json_data['attributes']['frontSide'] == 'What is MVC?'
    assert json_data['attributes']['backSide'] == 'stuff and things'

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

def xtest_cards_get_list():
    # Needs refactoring to make sure user and card with id's '1' are created before this is run
    response = app.test_client().get('api/v1/users/1/cards')
    json_data = json.loads(response.data)

    assert response.status_code == 200

    assert type(json_data['technicalCards']) == list
    assert json_data['technicalCards'][0]['type'] == 'flashCard'
    assert json_data['technicalCards'][0]['attributes']['category'] == 'technicalBE'
    assert type(json_data['technicalCards'][0]['attributes']['competenceRating']) == float
    assert type(json_data['technicalCards'][0]['attributes']['frontSide']) == str
    assert type(json_data['technicalCards'][0]['attributes']['backSide']) == str

    assert type(json_data['behavioralCards']) == list
    assert json_data['behavioralCards'][0]['type'] == 'flashCard'
    assert json_data['behavioralCards'][0]['attributes']['category'] == 'technicalBE'
    assert type(json_data['behavioralCards'][0]['attributes']['competenceRating']) == float
    assert type(json_data['behavioralCards'][0]['attributes']['frontSide']) == str
    assert type(json_data['behavioralCards'][0]['attributes']['backSide']) == str

def xtest_card_update_invalid_user_id():
    response = app.test_client().get('api/v1/users/1/cards')
    json_data = json.loads(response.data)

    assert response.status_code == 400

    assert json_data['error'] == 'no user found with the given id.'
