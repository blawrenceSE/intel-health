FROM alpine

LABEL maintainer blawrence

RUN apk add --update python py-pip bash

RUN pip install --upgrade pip requests
RUN pip install sendgrid

ADD health_monitor.py /
ADD day_diff.py /

CMD python health_monitor.py

