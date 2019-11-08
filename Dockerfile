FROM python:3-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y udev \ 
    && pip install . \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 9410

CMD [ "usb2container", "start" ]
