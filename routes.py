from flask import Flask, Response, request, send_file
from astral import LocationInfo
from pprint import pprint
from moviepy.video.VideoClip import TextClip
from moviepy.editor import CompositeVideoClip

from moviepy.video.io.VideoFileClip import VideoFileClip
import requests
from astral.sun import sun
from datetime import datetime, timedelta
from nptime import nptime
import os 
import cv2
import numpy as np
import glob
from time import sleep
from media import prepare_video


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

def create_opencv_image_from_stringio(images):
    for img_stream in images:
        img_stream.seek(0)
        image_bytes = img_stream.read()  
        decoded = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        yield decoded


@app.route('/post-story', methods = ['POST'])
def post_story():
    text = request.form.get('text')

    image_list = request.files.getlist('image')
    generator = create_opencv_image_from_stringio([image_list.pop()])
    first_image = next(generator)
    height, width, layers = first_image.shape
    size = (width,height)
    video_path = 'project.mp4'
    frames_per_second = len(image_list) / 12

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), frames_per_second, size)

    for img in create_opencv_image_from_stringio(image_list):
        out.write(img)

    out.release()

    prepare_video(video_path,   aspect_ratios=(3/4), max_duration=14.9,
            min_size=(612, 612), max_size=(1080, 1920), save_path='second.mp4')

    # TODO: set text a bit up from bottom
    text = TextClip(text,fontsize=44, color='white').set_position(("center")).set_duration(1)
    clip = VideoFileClip('second.mp4', audio=False)
    final_clip = CompositeVideoClip([clip, text])
    final_clip.write_videofile(video_path, fps=frames_per_second )
    text.close()    
    clip.close()
    final_clip.close()
    return send_file('project.mp4')