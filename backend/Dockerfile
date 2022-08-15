FROM python:3.10

WORKDIR /srv/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt /srv/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /srv/backend



