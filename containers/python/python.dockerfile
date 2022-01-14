# base python runtime container
FROM --platform=amd64 python:3.6.15-slim-buster

LABEL maintainer="support@ampcontrol.io"

WORKDIR /cryptoline

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH=/cryptoline
ENV PYTHONUNBUFFERED=1

COPY containers/postgres/postgres-wait.sh /bin/postgres-wait 
COPY requirements.txt .

RUN apt-get -y update
RUN apt-get -y install gnupg gnupg2 wget python3-dev build-essential wait-for-it

RUN echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get -y update
RUN apt-get -y install postgresql-client-13

RUN pip3 install -r requirements.txt

RUN rm /var/cache/* /root/.cache -rf

RUN apt-get -y purge '*-dev'
RUN apt clean all
