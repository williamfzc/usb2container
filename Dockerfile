FROM python:3-alpine3.7

WORKDIR /usr/src/app

RUN apk add --no-cache git \
    && pip install . \
    && apk add --no-cache udev \
    && apk add --no-cache bash

EXPOSE 9410

CMD [ "u2c_server", "start" ]
