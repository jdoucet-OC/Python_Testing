import pytest
from Python_Testing import server


@pytest.fixture
def client():
    """"""
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


def test_user(client):
    """"""
    wtr = client.get('/')

    assert wtr.status_code == 200
    wtr = client.post('/showSummary',
                      data={'email': 'admin@irontemple.com'})
    assert wtr.status_code == 200
    assert b"Welcome, admin@irontemple.com" in wtr.data
    assert b"Name : " in wtr.data

    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Fall Classic',
                            'places': '13'}
                      )
    assert b"Competition already over" in wtr.data
    assert b'You cannot book more than 12 places' in wtr.data
    assert b'Not enough points' in wtr.data

    club = [c for c in server.clubs if c['name'] == 'Iron Temple'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Futur Competition',
                            'places': '1'}
                      )
    updated_points = int(club['points'])
    assert wtr.status_code == 200
    assert updated_points == 1
    assert updated_points != points
    assert b"Name : " in wtr.data
