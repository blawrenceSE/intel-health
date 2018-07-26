FROM alpine

LABEL maintainer blawrence

RUN apk add --update python py-pip git bash

RUN pip install --upgrade pip


RUN git clone https://github.com/blawrencens/intel-health

CMD tail -f /dev/null
RUN python healh_monitor.py