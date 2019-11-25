#!/bin/bash
#
# Production farm start script
#
# NGINX<--UDS-->uWSGI<-->FLASK
#
# Define NGINX stuff
#
NGINX=/usr/sbin/nginx
NGINX_CONF=conf/nginx_uwsgi.conf
NGINX_ELOG=logs/nginx_elog.log
NGINX_ALOG=logs/nginx_alog.log
NGINX_PID=logs/nginx.pid
#
# Define uWSGI stuff
#
UWSGI=~/.local/bin/uwsgi
UWSGI_INI=conf/uwsgi.ini
UWSGI_PID=logs/uwsgi.pid
UWSGI_LOG=logs/uwsgi.log
#
# are we up already?
#
if [ -f $UWSGI_PID ]; then
    echo "App already running: $UWSGI_PID"
    echo "Use farm_stop.sh to shut."
    exit 1
fi
#
# rotate logs if not rotated yet
#
TIMESTAMP=`date "+%Y%m%d.%H%M%S"`
if [ -f $UWSGI_LOG ]; then
    echo "Backing up $UWSGI_LOG"
    mv "$UWSGI_LOG" "$UWSGI_LOG.$TIMESTAMP"
fi
if [ -f $NGINX_ELOG ]; then
    echo "Backing up $NGINX_ELOG"
    mv "$NGINX_ELOG" "$NGINX_ELOG.$TIMESTAMP"
fi
if [ -f $NGINX_ALOG ]; then
    echo "Backing up $NGINX_ALOG"
    mv "$NGINX_ALOG" "$NGINX_ALOG.$TIMESTAMP"
fi
#
# start uWSGI
#
$UWSGI --ini $UWSGI_INI
#
# Wait for the farm to be launched by uWSGI
echo -n Launching farm via uWSGI.
sleep 1
#echo -n ..
#sleep 1
#echo -n ..
#sleep 1
#echo -n ..
#sleep 1
echo .
#
# report progress
#
if [ -f $WSGI_PID ]; then
    pstree -p `cat $UWSGI_PID`
    echo "uWSGI log: $UWSGI_LOG"
fi
#
# start NGINX
#
echo "Starting NGINX..."
$NGINX -c $NGINX_CONF -p .
echo "NGINX log: $NGINX_ALOG"
echo "NGINX log: $NGINX_ELOG"
echo "Use farm_stop.sh to shut this service"
