FROM python:3-alpine3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install . \
    && apk add --no-cache udev \
    && apk add --no-cache bash

EXPOSE 9410

CMD [ "u2c_server", "start" ]
