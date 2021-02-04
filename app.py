from bottle import route, run, template
from astral import LocationInfo
from pprint import pprint
import requests
from astral.sun import sun
from datetime import datetime, timedelta
from nptime import nptime
def is_golden_hour(date_now, sunset, sunrise):
    sunset_end_range = sunset + timedelta(minutes=30)
    sunset_begin_range = sunset - timedelta(minutes=30)
    

    sunrise_end_range = sunrise + timedelta(minutes=30)
    sunrise_begin_range = sunrise - timedelta(minutes=30)
    
    is_sunrise = sunrise_begin_range < date_now < sunrise_end_range 
    is_sunset = sunset_begin_range < date_now < sunset_end_range 
    return is_sunrise or is_sunset


@route('/')
def index():
    time_data = requests.get("http://worldtimeapi.org/api/timezone/Europe/Berlin.json").json()
    now = datetime.fromisoformat(time_data["utc_datetime"])
    city = LocationInfo("Berlin", "Germany", "Europe/Berlin", 52.52, 13.4050)
    s = sun(city.observer, date=now)
    is_golden  = is_golden_hour(now,  s['sunrise'], s['sunset'])

    return {"golden_hour": is_golden}

run(host='localhost', port=8080)
