# syntax=docker/dockerfile:1.4
# pull official base image
FROM ubuntu:20.04

# set work directory
WORKDIR /opt/python-projects/app

# set non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libssl-dev \
    libffi-dev \
    python3-pip \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel and setuptools
RUN pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip

# download and install uv tool
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# setup virtual environment and install python dependencies
RUN python3 -m pip install torch==2.3.0+cpu torchvision==0.18.0+cpu torchaudio==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    && python3 -m pip install ultralytics --verbose

# copy requirements file
COPY ./requirements.txt /opt/python-projects/app/requirements.txt

# install project dependencies
RUN python3 -m pip install -r /opt/python-projects/app/requirements.txt --verbose

# copy project
COPY . /opt/python-projects/app/

# Optional: Uncomment to run commands on build
# RUN ls -la
# RUN PYTHONPATH=. alembic upgrade head