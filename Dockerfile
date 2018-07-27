FROM alpine

LABEL maintainer blawrence

RUN apk add --update python py-pip git bash

RUN pip install --upgrade pip requests


RUN git clone https://github.com/blawrencens/intel-health

RUN crontab -l | { cat; echo "*    *       *       *       *       /intel-health/run.sh"; } | crontab -

CMD tail -f /dev/null

#RUN python /intel-health/health_monitor.py
