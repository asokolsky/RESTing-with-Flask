#!/bin/bash
#
# Production farm start script
#
# Two configurations are possible:
#
# Client<-->NGINX<-->UDS<-->uWSGI<-->FLASK
#
# or
#
# Client<-->uWSGI<-->FLASK
#
# see lines maked "pick the config here"
#
# Define NGINX stuff
#
# pick the config here:
NGINX=/usr/sbin/nginx
#NGINX=/doesnotexist
NGINX_CONF=conf/nginx_uwsgi.conf
NGINX_ELOG=logs/nginx_elog.log
NGINX_ALOG=logs/nginx_alog.log
NGINX_PID=logs/nginx.pid
#
# Define uWSGI stuff
#
# pick the config here:
UWSGI_INI=conf/uwsgi_nginx.ini
#UWSGI_INI=conf/uwsgi_only.ini
UWSGI=~/.local/bin/uwsgi
UWSGI_PID=logs/uwsgi.pid
UWSGI_LOG=logs/uwsgi.log
#
# are we up already?
#
if [ -f $UWSGI_PID ]; then
    echo "Already running: $UWSGI_PID"
    echo "Use farm_stop.sh to shut."
    exit 1
fi
#
# rotate logs if not rotated yet
#
TIMESTAMP=`date "+%Y%m%d.%H%M%S"`

move_if_exists() {
    if [ -f $1 ]; then
        echo "Backing up $1"
        mv $1 "$1.$TIMESTAMP"
    fi
}

move_if_exists $UWSGI_LOG
move_if_exists $NGINX_ELOG
move_if_exists $NGINX_ALOG
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
    echo "Started uwsgi: " 
    pstree -p `cat $UWSGI_PID`
    echo "uWSGI log: $UWSGI_LOG"
fi
#
# start NGINX if $NGINX is a file
#
if [ -f $NGINX ]; then
    echo "Starting NGINX..."
    $NGINX -c $NGINX_CONF -p .
    echo "NGINX log: $NGINX_ALOG"
    echo "NGINX log: $NGINX_ELOG"
fi

echo "Use farm_stop.sh to shut this service"
