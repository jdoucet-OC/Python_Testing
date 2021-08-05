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
    club = [c for c in server.clubs if c['name'] == 'Iron Temple'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Spring Festival',
                            'places': '3'}
                      )
    updated_points = int(club['points'])
    assert points != updated_points


def test_bad_points(client):
    """"""
    club = [c for c in server.clubs if c['name'] == 'Iron Temple'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Iron Temple',
                            'competition': 'Spring Festival',
                            'places': '5'}
                      )
    updated_points = int(club['points'])
    assert updated_points == points


def test_thirteen_points(client):
    """"""
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Spring Festival',
                            'places': '13'}
                      )
    updated_points = int(club['points'])
    assert updated_points == points


def test_twelve_points(client):
    """"""
    club = [c for c in server.clubs if c['name'] == 'Simply Lift'][0]
    points = int(club['points'])
    wtr = client.post('/purchasePlaces',
                      data={'club': 'Simply Lift',
                            'competition': 'Spring Festival',
                            'places': '12'}
                      )
    updated_points = int(club['points'])
    assert updated_points != points