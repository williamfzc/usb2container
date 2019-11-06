FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install .

EXPOSE 9410

CMD [ "u2c_server", "start" ]
