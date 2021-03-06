from flask import Flask, Response, request, send_file
from astral import LocationInfo
from pprint import pprint
from moviepy.video.VideoClip import TextClip
from moviepy.editor import CompositeVideoClip
import logging
from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
from astral.sun import sun, sunrise
from datetime import datetime, timedelta
from nptime import nptime
import os
import cv2
import numpy as np
import glob
from time import sleep
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import pytz  # 3rd party: $ pip install pytz


retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def is_golden_hour(date_now, sunset, sunrise):
    sunset_end_range = sunset + timedelta(minutes=30)
    sunset_begin_range = sunset - timedelta(minutes=30)

    sunrise_end_range = sunrise + timedelta(minutes=30)
    sunrise_begin_range = sunrise - timedelta(minutes=30)

    is_sunrise = sunrise_begin_range < date_now < sunrise_end_range
    is_sunset = sunset_begin_range < date_now < sunset_end_range
    return is_sunrise or is_sunset


@app.route('/', )
def index():
    request_ip = request.remote_addr
    source_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    app.logger.info({'request_ip': request_ip, 'source_ip': source_ip})

    u = datetime.utcnow()
    # NOTE: it works only with a fixed utc offset
    now = u.replace(tzinfo=pytz.utc)

    city = LocationInfo("Berlin", "Germany", "Europe/Berlin", 52.52, 13.4050)
    s = sun(city.observer, date=now)
    is_golden = is_golden_hour(now,  s['sunrise'], s['sunset'])

    return {"golden_hour": is_golden,
            "berlin": {
                "sunrise": s['sunrise'],
                "sunset": s['sunset'],
                "now": now,
            }

            }
