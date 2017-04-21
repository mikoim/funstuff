FROM ubuntu:xenial
MAINTAINER Eshin Kunishima <ek@esh.ink>

RUN apt-get update && \
    apt-get install -y nginx python3 python3-pip supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /srv/subot

RUN bash /srv/subot/contrib/setup.sh

EXPOSE 80
CMD ["/usr/bin/supervisord"]
