#!/usr/bin/env bash

APPNAME=codexpose
APPDIR=$PWD/backend/codexpose/

LOGFILE=$APPDIR'gunicorn.log'
ERRORFILE=$APPDIR'gunicorn-error.log'

NUM_WORKERS=3
TIMEOUT=120

ADDRESS=127.0.0.1:8000

cd $APPDIR

exec gunicorn $APPNAME.wsgi:application \
-w $NUM_WORKERS --bind=$ADDRESS \
--timeout $TIMEOUT \
--log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE  1>>$ERRORFILE &

# As the gunicorn server will run in background, to stop the python server run:
# sudo fuser -k 8000/tcp