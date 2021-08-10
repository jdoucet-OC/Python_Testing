import pytest
from .. import server


@pytest.fixture
def client():
    """"""
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


def test_good_email(client):
    """"""
    wtr = client.post('/showSummary',
                           data={'email': 'admin@irontemple.com'})
    assert wtr.status_code == 200


def test_bad_email(client):
    """"""
    wtr = client.post('/showSummary',
                           data={'email': 'email@wrong.test'})
    assert wtr.status_code == 302


def test_good_points(client):
    """"""
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Futur Competition',
                            'places': '3'}
                      )
    assert wtr.status_code == 200


def test_bad_points(client):
    """"""
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Futur Competition',
                            'places': '5'}
                      )
    message = b"Not enough points"
    assert message in wtr.data


def test_thirteen_points(client):
    """"""
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '13'}
                      )
    message = b"You cannot book more than 12 places"
    assert message in wtr.data


def test_twelve_points(client):
    """"""
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '12'}
                      )
    assert wtr.status_code == 200


def test_past_competition(client):
    """"""
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Fall Classic',
                            'places': '12'}
                      )
    message = b"Competition already over"
    assert message in wtr.data


def test_points_update(client):
    """"""
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '1'}
                      )
    updated_points = int(club['points'])
    assert updated_points != points
