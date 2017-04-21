#!/bin/sh

CONTRIB=`dirname "${0}"`
NGINX=/usr/sbin/nginx
PIP3=/usr/bin/pip3

# nginx
cd /etc/nginx/sites-enabled && \
rm default && \
ln -s "${CONTRIB}/nginx.conf" subot && \
${NGINX} -t && \
# subot
${PIP3} install --upgrade pip && \
${PIP3} install -r "${CONTRIB}/../requirements.txt" && \
# supervisord
cd /etc/supervisor/conf.d && \
ln -s "${CONTRIB}/supervisord.conf" subot.conf
