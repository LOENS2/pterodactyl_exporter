import argparse
from os import environ
import time

import HttpClient
import HttpServer
import envLoad


def parse_args():
    parser = argparse.ArgumentParser(description="environment file")
    parser.add_argument("--env-file")
    envFile = parser.parse_args().env_file
    if envFile is None:
        envFile = ".env"
    envLoad.envLoad(envFile)


if __name__ == '__main__':
    parse_args()

    HttpClient.client_init()

    HttpServer.init_metrics()

    while True:
        HttpClient.get_server()
        metrics = HttpClient.get_metrics()
        HttpServer.serve_metrics(metrics)
        time.sleep(10)