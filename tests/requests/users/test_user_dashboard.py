from app import app, db
from models.user import User
from models.card import Card
import json

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

