#!/bin/sh

CONTRIB=`dirname "${0}"`
ARUKAS=./arukas

wget -O arukas.zip "https://github.com/arukasio/cli/releases/download/v${ARUKAS_VERSION}/arukas_v${ARUKAS_VERSION}_linux_amd64.zip"
unzip arukas.zip

CONTAINER_ID=`"${ARUKAS}" ps | grep -i subot.arukascloud.io | cut -f 1`

if [ ! -z "${CONTAINER_ID}" ]; then
    "${ARUKAS}" stop "${CONTAINER_ID}"
else
    echo 'subot container has gone away.' 1>&2
	exit 1
fi

"${ARUKAS}" start "${CONTAINER_ID}"
