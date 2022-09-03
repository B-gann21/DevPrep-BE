from app import app, db
from models.user import User
from models.card import Card
import json

def test_login_user():
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

    for u in User.query.all():
        db.session.delete(u)
        db.session.commit()
