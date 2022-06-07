from prometheus_client import start_http_server, Gauge

label_names = ("server_name", "id",)

memory = Gauge("pterodacytl_server_memory_bytes", "Memory used by server in bytes", label_names)
cpu = Gauge("pterodactyl_server_cpu_absolute", "Absolute cpu usage by server", label_names)
disk = Gauge("pterodactyl_server_disk_bytes", "Disk space used by server in bytes", label_names)
rx = Gauge("pterodactyl_server_network_rx_bytes", "Bytes received by server via network", label_names)
tx = Gauge("pterodactyl_server_network_tx_bytes", "Bytes transmitted by server via network", label_names)
uptime = Gauge("pterodactyl_server_uptime_seconds", "Server uptime in seconds", label_names)


def init_metrics():
    start_http_server(8000)


def serve_metrics(metrics):
    len(metrics["id"])
    for x in range(len(metrics["id"])):
        srv_label = metrics['name'][x]
        id_label = metrics['id'][x]
        memory.labels(srv_label, id_label).set(metrics["memory"][x])
        cpu.labels(srv_label, id_label).set(metrics["cpu"][x])
        disk.labels(srv_label, id_label).set(metrics["disk"][x])
        rx.labels(srv_label, id_label).set(metrics["rx"][x])
        tx.labels(srv_label, id_label).set(metrics["tx"][x])
        uptime.labels(srv_label, id_label).set(metrics["uptime"][x])