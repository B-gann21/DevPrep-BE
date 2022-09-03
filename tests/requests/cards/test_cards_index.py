from app import app, db
from models.user import User
from models.card import Card
import json

def test_cards_get_list():
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
