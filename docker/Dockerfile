# syntax=docker/dockerfile:1

FROM python:3-alpine

WORKDIR /opt/pterodactyl_exporter/app

RUN mkdir -p /opt/pterodactyl_exporter/config

RUN pip3 install pterodactyl-exporter

# Fixes ModuleNotFoundError, remove after next line after bug has been fixed (see https://github.com/LOENS2/pterodactyl_exporter/issues/4)
RUN pip3 install prometheus_client

CMD [ "pterodactyl_exporter", "--config-file=/opt/pterodactyl_exporter/config/config.yml" ]

EXPOSE 9531
