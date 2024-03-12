import argparse
import http.client
import time
import sys
import datetime

from pterodactyl_exporter import config_load, http_client, http_server


def parse_args():
    parser = argparse.ArgumentParser(description="config file")
    parser.add_argument("--config-file", default="config.yml")
    cfg_file = parser.parse_args().config_file
    if cfg_file is None:
        print("No config provided!")
        exit(1)
    return cfg_file


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    config_file = parse_args()
    config = config_load.get_config(config_file)
    http_client.client_init(config)
    http_server.init_metrics(config)

    print("Init successful!")

    while True:
        try:
            http_client.get_server(config["server_list_type"])
            metrics = http_client.get_metrics()
            http_server.serve_metrics(metrics)
            print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} | Served metrics")
            time.sleep(10)
        except http.client.RemoteDisconnected:
            print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} | API not responding!")
            time.sleep(10)
            continue
        except Exception as e:
            print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} | An error occured:")
            print(e)
            time.sleep(10)
            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Script stopped!")
        raise SystemExit
