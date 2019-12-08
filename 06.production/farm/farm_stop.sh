#!/bin/bash
#
# Production farm stop script
# Works for either of the two possible configs
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
UWSGI=~/.local/bin/uwsgi
UWSGI_PID=logs/uwsgi.pid
UWSGI_LOG=logs/uwsgi.log
#
# stop NGINX
#
if [ -f $NGINX_PID ]; then
    echo "Stopping NGINX.."
    $NGINX -c $NGINX_CONFIG -p . -s stop
#else
#    echo "Can't find $NGINX_PID"
fi
#
# stop uWSGI
#
if [ -f $UWSGI_PID ]; then
    echo "Stopping uWSGI.."
    $UWSGI --stop $UWSGI_PID
else
    echo "Can't find $UWSGI_PID"
fi
# for some reason once is not enouhg ;-(
#if [ -f $UWSGI_PID ]; then
#    echo "Stopping uWSGI.."
#    $UWSGI --stop $UWSGI_PID
#fi
#
# rotate the NGINX & uWSGI logs
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
