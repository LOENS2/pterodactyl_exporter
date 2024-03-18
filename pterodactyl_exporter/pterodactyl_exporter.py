import argparse
import http.client
import time
from .console_logger import log_to_console
from .config_load import get_config
from .http_client import HTTPClient
from .http_server import HTTPServer


def get_config_file_path():
    parser = argparse.ArgumentParser(description="config file")
    parser.add_argument("--config-file", default="config.yml")
    return parser.parse_args().config_file


def main():
    config_path = get_config_file_path()
    try:
        config = get_config(config_path)
    except FileNotFoundError:
        log_to_console(f"Config file in path {config_path} not found, please provide one!", True, True)
        raise SystemExit
    except ValueError as e:
        log_to_console("Config Error:", True, True, e)
        raise SystemExit

    http_client = HTTPClient(config)
    http_server = HTTPServer(config)

    log_to_console("Init successful!")

    while True:
        try:
            metrics = http_client.get_metrics()
            http_server.serve_metrics(metrics)
            log_to_console("Serverd metrics")
            time.sleep(10)
        except http.client.RemoteDisconnected:
            log_to_console("API not responding!", True)
            time.sleep(10)
            continue
        except Exception as e:
            log_to_console("An error occurred:", True, False, e)
            time.sleep(10)
            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log_to_console("Keyboard Interrupt", False, True)
        raise SystemExit
