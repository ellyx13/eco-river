# pull official base image
FROM python:3.11-alpine

# set work directory
WORKDIR /opt/python-projects/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# install base dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    ffmpeg \
    && pip install --upgrade pip setuptools wheel \
    && rm -rf /root/.cache/pip \
    && pip install --upgrade pip

# download and install uv tool
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# setup virtual environment and install python dependencies
RUN /root/.cargo/bin/uv venv /opt/venv \
    && pip install torch==2.3.0+cpu torchvision==0.18.0+cpu torchaudio==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    && pip install ultralytics --verbose

# copy requirements file
COPY ./requirements.txt /opt/python-projects/app/requirements.txt

# install project dependencies
RUN /root/.cargo/bin/uv pip install -r /opt/python-projects/app/requirements.txt --verbose


# copy project
COPY . /opt/python-projects/app/
# RUN ls -la
# RUN PYTHONPATH=. alembic upgrade head