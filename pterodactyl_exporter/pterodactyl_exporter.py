import argparse
import http.client
import time

import http_client
import http_server
import config_load


def parse_args():
    parser = argparse.ArgumentParser(description="environment file")
    parser.add_argument("--config-file")
    config_file = parser.parse_args().config_file
    if config_file is None:
        print("No config provided!")
        exit(1)
    return config_file


if __name__ == '__main__':
    config_file = parse_args()

    config = config_load.get_config(config_file)

    http_client.client_init(config)

    http_server.init_metrics()

    while True:
        try:
            http_client.get_server()
            metrics = http_client.get_metrics()
            http_server.serve_metrics(metrics)
            time.sleep(10)
        except http.client.RemoteDisconnected:
            print("API does not respond!")
        finally:
            continue
