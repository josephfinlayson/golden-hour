from datetime import datetime
from app import is_golden_hour, index

def test_if_golden_hour_test():

    now = datetime(2020, 1, 1, hour=12, minute=15)
    sunset = datetime(2020, 1, 1, hour=12, minute=16)
    sunrise = datetime(2020, 1, 1, hour=12, minute=14)

    assert is_golden_hour(now, sunset, sunrise) == True

def test_index_test():
    answer = index()
    g = list(answer).pop()

    assert g == 'golden_hour'