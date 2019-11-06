FROM python:3-alpine

WORKDIR /usr/src/app

COPY . .

RUN apk add build-base \
    && pip install . \
    && apk add udev \
    && apk del build-base

EXPOSE 9410

CMD [ "u2c_server", "start" ]
