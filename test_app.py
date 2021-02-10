from datetime import datetime
from routes import is_golden_hour, index, post_story, app
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

SMALLEST_JPEG_B64 = """\
/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8Q
EBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g/9k=
"""


def test_image_to_video(client):
    f = open('./sample.jpg', 'rb') 
    f2 = open('./sample_2.jpg', 'rb') 
    f.seek(0)
    f2.seek(0)

    response = client.post('/post-story', data=dict(image =[f, f2], text="test1"))
    assert response.headers['Content-Type'] == 'video/mp4'