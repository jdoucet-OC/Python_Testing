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
