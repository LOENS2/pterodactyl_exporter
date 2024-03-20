from prometheus_client import Gauge, start_http_server
from .dto.config import Config
from .dto.metrics import Metrics


class HTTPServer:
    def __init__(self, config: Config):
        start_http_server(config.port)

        label_names = ("server_name", "id",)

        self.metric_gauges = {
            "memory": Gauge("pterodactyl_server_memory_mebibyte", "Memory used by server in mebibyte", label_names),
            "cpu": Gauge("pterodactyl_server_cpu_absolute", "Absolute cpu usage by server", label_names),
            "disk": Gauge("pterodactyl_server_disk_mebibyte", "Disk space used by server in mebibyte", label_names),
            "rx": Gauge("pterodactyl_server_network_rx_mebibyte", "Mebibyte received by server via network", label_names),
            "tx": Gauge("pterodactyl_server_network_tx_mebibyte", "Mebibyte transmitted by server via network", label_names),
            "uptime": Gauge("pterodactyl_server_uptime_milliseconds", "Server uptime in milliseconds", label_names),
            "max_memory": Gauge("pterodactyl_server_max_memory_mebibyte", "Maximum memory allocated to server in mebibyte", label_names),
            "max_swap": Gauge("pterodactyl_server_max_swap_mebibyte", "Maximum swap allocated to server in mebibyte", label_names),
            "max_disk": Gauge("pterodactyl_server_max_disk_mebibyte", "Maximum disk space allocated to server in mebibyte", label_names),
            "io": Gauge("pterodactyl_server_io", "IO weight of server", label_names),
            "max_cpu": Gauge("pterodactyl_server_max_cpu_absolute", "Maximum cpu load allowed to server", label_names),
            "last_backup_time": Gauge("pterodactyl_server_most_recent_backup_time", "Timestamp of the most recent backup", label_names)
        }

    def serve_metrics(self, metrics: Metrics):
        for index in range(len(metrics.name)):
            srv_label = metrics.name[index]
            id_label = metrics.id[index]
            for metric_name, value in metrics.__dict__.items():
                if metric_name not in ['name', 'id']:
                    self.metric_gauges[metric_name].labels(srv_label, id_label).set(value[index])
