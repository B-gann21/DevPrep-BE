from app import app, db
from models.user import User
from models.card import Card
import json

def test_average_card_ratings():
    user = User(username='coolguy123', email='coolguy123@gmail.com')
    fe_card1 = Card(category='technicalFE', front='an FE question', rating=5)
    fe_card2 = Card(category='technicalFE', front='an FE question', rating=4)
    be_card1 = Card(category='technicalBE', front='a BE question', rating=5)
    be_card2 = Card(category='technicalBE', front='a BE question', rating=3)
    behav_card1 = Card(category='behavioral', front='a behavioral question', rating=4)
    behav_card2 = Card(category='behavioral', front='a behavioral question', rating=3)
    cards = [fe_card1, fe_card2, be_card1, be_card2, behav_card1, behav_card2]
    for card in cards:
        user.cards.append(card)

    db.session.add(user)
    db.session.commit()

    assert user.average_card_rating_by_category('technicalBE') == 4.0
    assert user.average_card_rating_by_category('technicalFE') == 4.5
    assert user.average_card_rating_by_category('behavioral') == 3.5

def test_generate_default_cards():
    user = User(
        username='Billy Jo',
        email='billyjo@billyjo.com'
    )
    db.session.add(user)
    db.session.commit()

    assert user.cards == []

    user.generate_default_cards()

    assert len(user.cards) == 130
