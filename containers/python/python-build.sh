#!/bin/sh

set -e
set -x

export DEBIAN_FRONTEND=noninteractive

apt-get -y update
apt-get -y install gnupg gnupg2 wget python3-dev build-essential
echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

apt-get -y update
apt-get -y install \
        postgresql-client-13 \
        wait-for-it

pip3 install -r requirements.txt

rm /var/cache/* /root/.cache -rf

apt-get -y purge '*-dev'
apt clean all
