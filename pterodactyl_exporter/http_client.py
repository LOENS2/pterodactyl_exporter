import requests
import time
import dateutil.parser
from .dto.config import Config
from .dto.metrics import Metrics


class HTTPClient:
    def __init__(self, config: Config):
        self.config = config
        self.metrics: Metrics = Metrics()
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_metrics(self):
        self.metrics = Metrics()
        t1 = time.time()
        servers = self.fetch_server()
        pages = servers['meta']['pagination']['total_pages']
        for server_data in servers.get('data', []):
            if not (bool(server_data['attributes']['is_suspended']) or
                    bool(server_data['attributes']['is_installing'])):
                self.process_servers(server_data)

        for page in range(pages):
            for index, server_id in enumerate(self.metrics.id):
                resources = self.fetch_resources(server_id, index, page + 1)
                self.process_resources(resources)
                self.fetch_last_backup_time(server_id, index, page + 1)
        t2 = time.time()
        print(f"total= {t2 - t1}")
        return self.metrics

    def fetch_server(self):
        url = f"{self.get_url()}/api/client/?type={self.config.server_list_type}"
        response = requests.get(url, headers=self.headers, verify=not self.config.ignore_ssl)
        if response.status_code != 200:
            raise Exception(f"Error fetching servers: {response.text}")
        response.close()
        return response.json()

    def process_servers(self, server_data):
        attributes = server_data.get('attributes', {})
        self.metrics.name.append(attributes.get('name', ''))
        self.metrics.id.append(attributes.get('identifier', ''))
        self.metrics.max_memory.append(attributes['limits']['memory'])
        self.metrics.max_swap.append(attributes['limits']['swap'])
        self.metrics.max_disk.append(attributes['limits']['disk'])
        self.metrics.io.append(attributes['limits']['io'])
        self.metrics.max_cpu.append(attributes['limits']['cpu'])

    def fetch_resources(self, server_id, index, page):
        url = f"{self.get_url()}/api/client/servers/{server_id}/resources?page={page}"
        response = requests.get(url, headers=self.headers, verify=not self.config.ignore_ssl)
        if response.status_code != 200:
            raise Exception(f"Fetch metrics for {self.metrics.name[index]}")
        response_data = response.json()
        response.close()
        return response_data["attributes"]["resources"]

    def process_resources(self, resources):
        self.metrics.memory.append(self.convert_byte_to_mebibyte(resources["memory_bytes"]))
        self.metrics.cpu.append(resources["cpu_absolute"])
        self.metrics.disk.append(self.convert_byte_to_mebibyte(resources["disk_bytes"]))
        self.metrics.rx.append(self.convert_byte_to_mebibyte(resources["network_rx_bytes"]))
        self.metrics.tx.append(self.convert_byte_to_mebibyte(resources["network_tx_bytes"]))
        self.metrics.uptime.append(resources["uptime"])

    def fetch_last_backup_time(self, server_id, index, page):
        url = f"{self.get_url()}/api/client/servers/{server_id}/backups?per_page=50&page={page}"
        response = requests.get(url, headers=self.headers, verify=not self.config.ignore_ssl)
        if response.status_code != 200:
            raise Exception(f"Fetch last backup for {self.metrics.name[index]}")
        response_data = response.json()
        response.close()
        backups = response_data["data"]
        last_successful_backup = max(
            dateutil.parser.isoparse(backup["attributes"]["completed_at"]).timestamp()
            for backup in backups
            if backup["attributes"]["is_successful"]
        ) if backups else 0
        self.metrics.last_backup_time.append(last_successful_backup)

    def get_url(self):
        if self.config.https:
            return f"https://{self.config.host}:443"
        return f"http://{self.config.host}:80"

    @staticmethod
    def convert_byte_to_mebibyte(byte):
        return byte / 1048576
