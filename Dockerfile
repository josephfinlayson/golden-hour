FROM python:3.8-slim

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 imagemagick  -y

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]

