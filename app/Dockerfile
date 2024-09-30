# pull official base image
FROM python:3.12-slim

# set work directory
WORKDIR /opt/python-projects/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS rtsp_transport;udp

# install dependencies
RUN apt-get update && apt-get install -y iputils-ping telnet ffmpeg libsm6 libxext6 libssl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip \
    && pip install --upgrade pip

# copy requirements file
COPY ./requirements.txt /opt/python-projects/app/requirements.txt

RUN pip install -r /opt/python-projects/app/requirements.txt

# Install curl for healthcheck
RUN apt-get install -y curl

# copy project
COPY . /opt/python-projects/app/
# RUN ls -la
# RUN PYTHONPATH=. alembic upgrade head