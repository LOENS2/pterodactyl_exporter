# syntax=docker/dockerfile:1

FROM python:3-alpine

WORKDIR /opt/pterodactyl_exporter/app

RUN mkdir -p /opt/pterodactyl_exporter/config

COPY . /opt/pterodactyl_exporter/app

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m", "pterodactyl_exporter.pterodactyl_exporter", "--config-file=/opt/pterodactyl_exporter/config/config.yml" ]

EXPOSE 9531/TCP
