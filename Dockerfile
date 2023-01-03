FROM python:3.8-buster
RUN apt-get update
RUN apt-get install -y python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /tmp/uploads

COPY src/ .

EXPOSE 80

ENTRYPOINT ["python", "app.py"]