import pytest
from Python_Testing import server


@pytest.fixture
def client():
    """"""
    flask_app = server.app
    with flask_app.test_client() as client:
        yield client


def test_good_email(client):
    """
    Tests website connection with known email
    :return: 200 OK
    """
    wtr = client.post('/showSummary',
                      data={'email': 'admin@irontemple.com'})
    assert wtr.status_code == 200


def test_bad_email(client):
    """
    Tests website connection with unknown email
    :return: 302 Redirect
    """
    wtr = client.post('/showSummary',
                      data={'email': 'email@wrong.test'})
    assert wtr.status_code == 302


def test_good_points(client):
    """
    Tests the purchasing of 3 places, in a valid competition
    with valid number of points
    :return: 200 OK
    """

    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Futur Competition',
                            'places': '3'}
                      )
    assert wtr.status_code == 200


def test_bad_points(client):
    """
    Tests the purchasing of 5 places, in a valid competition
    with invalid number of points
    :return: Error message flashed
    """
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Futur Competition',
                            'places': '5'}
                      )
    message = b"Not enough points"
    assert message in wtr.data


def test_thirteen_points(client):
    """
    Tests the purchase of too many places
    :return: Error message flashed
    """
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '13'}
                      )
    message = b"You cannot book more than 12 places"
    assert message in wtr.data


def test_twelve_points(client):
    """
    Tests the purchase of the maximum amount of places
    :return: 200 OK
    """
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '12'}
                      )
    assert wtr.status_code == 200


def test_points_null(client):
    """
    Tests the purchage of 0 points
    :return: points updated
    """
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Futur Competition',
                            'places': '0'}
                      )
    assert wtr.status_code == 200


def test_past_competition(client):
    """
    Tests the purchase of places in a past competition
    :return: Error message flashed
    """
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Fall Classic',
                            'places': '12'}
                      )
    message = b"Competition already over"
    assert message in wtr.data


def test_points_update(client):
    """
    Tests wether points are updated after a valid purchase
    :return: points updated
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


def test_point_display(client):
    """
    Verifies wether or not the display board is displayed
    :return: Valid http data
    """
    wtr = client.post('/showSummary',
                      data={'email': 'admin@irontemple.com'})
    points = b"Name : "
    assert points in wtr.data


def test_logout(client):
    """"""
    wtr = client.get('/')
    assert wtr.status_code == 200
