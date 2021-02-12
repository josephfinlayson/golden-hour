FROM python:3.9.1-slim

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 imagemagick  -y

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
  

ARG imagemagic_config=/etc/ImageMagick-6/policy.xml
RUN if [ -f $imagemagic_config ] ; then sed -i 's/domain="path" rights="none"/domain="path" rights="read|write"/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi

CMD [ "python", "./app.py" ]

