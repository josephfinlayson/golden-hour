from flask import Flask, Response, request, send_file
from astral import LocationInfo
from pprint import pprint
import requests
from astral.sun import sun
from datetime import datetime, timedelta
from nptime import nptime
import os 
import cv2
import numpy as np
import glob
from time import sleep


app = Flask(__name__)

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
    time_data = requests.get("http://worldtimeapi.org/api/timezone/Europe/Berlin.json").json()
    now = datetime.fromisoformat(time_data["utc_datetime"])
    city = LocationInfo("Berlin", "Germany", "Europe/Berlin", 52.52, 13.4050)
    s = sun(city.observer, date=now)
    is_golden  = is_golden_hour(now,  s['sunrise'], s['sunset'])

    return {"golden_hour": is_golden}

def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    image_bytes = img_stream.read()  
    decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    return decoded


@app.route('/post-story', methods = ['POST'])
def post_story():
    images = request.files.get('image')
    name, ext = os.path.splitext(images.filename)

    if ext not in ('.jpg','.jpeg'):
        return 'File extension not allowed.'

    processed_img_array = []
    for file in request.files.getlist('image'):
        img = create_opencv_image_from_stringio(file)
        height, width, layers = img.shape
        size = (width,height)
        processed_img_array.append(img)

    frames_per_second = len(request.files.getlist('image')) / 10
    out = cv2.VideoWriter('project.mp4', cv2.VideoWriter_fourcc(*'MP4V'), frames_per_second, size)

    for i in range(len(processed_img_array)) :
        out.write(processed_img_array[i])

    out.release()

    return send_file('project.mp4')

