import pytest
from Python_Testing import server


@pytest.fixture
def client():
    """"""
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


def test_triple_point(client):
    """
    Tests wether points are updated after a valid purchase
    Tests if they are valued at 3
    Tests if the status code is 200
    :return: points updated, 3 points = 1 place, HTTP 200 OK
    """
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '1'}
                      )
    updated_points = int(club['points'])
    assert updated_points != points
    assert updated_points-3 != points
    assert wtr.status_code == 200


def test_full_messages(client):
    """
    Tests all purchase errors
    verifies that points didn't change
    :return: all flashed messages in data
    """
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Fall Classic',
                            'places': '13'}
                      )
    updated_points = int(club['points'])
    assert updated_points == points
    assert b"Competition already over" in wtr.data
    assert b'You cannot book more than 12 places' in wtr.data
    assert b'Not enough points' in wtr.data


def test_full_login(client):
    """
    Tests website connection with known email
    verifies HTML
    :return: 200 OK, HTML Ok
    """
    wtr = client.post('/showSummary',
                      data={'email': 'admin@irontemple.com'})
    assert wtr.status_code == 200
    assert b"Name : " in wtr.data
    assert b"Welcome" in wtr.data