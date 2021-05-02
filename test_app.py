from datetime import datetime
from routes import is_golden_hour, index, app
import pytest
import werkzeug
import io
import base64

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_if_golden_hour_test():

    now = datetime(2020, 1, 1, hour=12, minute=15)
    sunset = datetime(2020, 1, 1, hour=12, minute=16)
    sunrise = datetime(2020, 1, 1, hour=12, minute=14)

    assert is_golden_hour(now, sunset, sunrise) == True

def test_index_test(client):
    answer = client.get('/').json
    print(answer)
    g = list(answer).pop()

    assert g == 'golden_hour'