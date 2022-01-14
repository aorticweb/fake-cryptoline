#!/bin/sh
exec \
  /usr/bin/wait-for-it -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -t 10 -- $@