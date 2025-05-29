# syntax=docker/dockerfile:1

FROM python:3-alpine

WORKDIR /pterodactyl_exporter

COPY dist/*.whl /pterodactyl_exporter

RUN pip3 install *.whl

RUN mkdir -p /opt/pterodactyl_exporter/config

CMD [ "python3", "-m", "pterodactyl_exporter.pterodactyl_exporter", "--config-file=/opt/pterodactyl_exporter/config/config.yml" ]

EXPOSE 9531/TCP
