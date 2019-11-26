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
# rotate the NGINX logs
#
TIMESTAMP=`date "+%Y%m%d.%H%M%S"`
if [ -f $NGINX_ELOG ]; then
    echo "Backing up $NGINX_ELOG"
    mv "$NGINX_ELOG" "$NGINX_ELOG.$TIMESTAMP"
fi
if [ -f $NGINX_ALOG ]; then
    echo "Backing up $NGINX_ALOG"
    mv "$NGINX_ALOG" "$NGINX_ALOG.$TIMESTAMP"
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
if [ -f $UWSGI_PID ]; then
    echo "Stopping uWSGI.."
    $UWSGI --stop $UWSGI_PID
fi
#
# rotate the uWSGI logs
#
if [ -f $UWSGI_LOG ]; then
    echo "Backing up $UWSGI_LOG"
    mv "$UWSGI_LOG" "$UWSGI_LOG.$TIMESTAMP"
fi
