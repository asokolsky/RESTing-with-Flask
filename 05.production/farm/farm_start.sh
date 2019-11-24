#!/bin/bash
#
# Production farm start script: NGINX-UDS->uWSGI->FLASK
#
# Define NGINX stuff
#
NGINX=/usr/sbin/nginx
NGINX_CONFIG=conf/nginx_uwsgi.conf
NGINX_ELOG=logs/nginx_elog.log
NGINX_ALOG=logs/nginx_alog.log
NGINX_PID=logs/nginx.pid
#
# Define uWSGI stuff
#
UWSGI=/usr/bin/uwsgi
# in the conf folder!
UWSGI_FLASK_CONFIG=farm_uwsgi.cfg
UWSGI_PID=logs/uwsgi.pid
UWSGI_LOG=logs/uwsgi.log
#
# socket for NGINX to talk to uWSGI, also used in NGINX_CONFIG
SOCKET=/var/tmp/farm.socket
#
# are we up already?
#
if [ -f $UWSGI_PID]; then
    echo "App already running: $UWSGI_PID"
    echo "Use farm_stop.sh to shut."
    exit 1
fi
#
# rotate NGINX logs is not rotated yet
#
TIMESTAMP=`date "+%Y%m%d.%H%M%S"`
if [ -f $UWSGI_LOG]; then
    echo "Backing up $UWSGI_LOG"
    mv "$UWSGI_LOG" "$UWSGI_LOG.$TIMESTAMP"
fi
if [ -f $NGINX_ELOG]; then
    echo "Backing up $NGINX_ELOG"
    mv "$NGINX_ELOG" "$NGINX_ELOG.$TIMESTAMP"
fi
if [ -f $NGINX_ALOG]; then
    echo "Backing up $NGINX_ALOG"
    mv "$NGINX_ALOG" "$NGINX_ALOG.$TIMESTAMP"
fi
#
# start uWSGI
#
$UWSGI \
    --uwsgi-socket $SOCKET \
    --master --processes 2 --threads 2 \
    --module=app.wsgi:app \
    --callable app \
    --pid-file "$WSGI_PID" \
    --daemonize="$WSGI_LOG" \
    --vacuum \
    --env FLASK_CONFIG="$UWSGI_FLASK_CONFIG"

# Wait for the farm to be launched by uWSGI
echo -n Launching farm via uWSGI.
sleep 1
echo -n ..
sleep 1
echo -n ..
sleep 1
echo
#
# report progress
#
if [ -f $WSGI_PID ]; then
    pstree -p `cat $WSGI_PID`
    echo "uWSGI log: $WSGI_LOG"
fi
#
# start NGINX
#
echo "Starting NGINX..."
$NGINX -c $NGINX_CONFIG -p .
echo "NGINX log: $NGINX_ALOG"
echo "NGINX log: $NGINX_ELOG"
echo "Use farm_stop.sh to shut this service"
