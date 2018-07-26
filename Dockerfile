FROM alpine

LABEL maintainer blawrence

RUN apk add --update python py-pip git bash

RUN pip install --upgrade pip requests


RUN git clone https://github.com/blawrencens/intel-health

RUN crontab -l | { cat; echo "*    *       *       *       *       /intel-health/run.sh"; } | crontab -
RUN chmod 777 /intel-health/run.sh
CMD tail -f /dev/null
