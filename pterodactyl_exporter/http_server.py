from prometheus_client import Gauge, start_http_server


label_names = ("server_name", "id",)

memory = Gauge("pterodacytl_server_memory_megabytes", "Memory used by server in megabytes", label_names)
cpu = Gauge("pterodactyl_server_cpu_absolute", "Absolute cpu usage by server", label_names)
disk = Gauge("pterodactyl_server_disk_megabytes", "Disk space used by server in megabytes", label_names)
rx = Gauge("pterodactyl_server_network_rx_megabytes", "Megabytes received by server via network", label_names)
tx = Gauge("pterodactyl_server_network_tx_megabytes", "Megabytes transmitted by server via network", label_names)
uptime = Gauge("pterodactyl_server_uptime_milliseconds", "Server uptime in milliseconds", label_names)
max_memory = Gauge("pterodactyl_server_max_memory_megabytes", "Maximum memory allocated to server in megabytes", label_names)
max_swap = Gauge("pterodactyl_server_max_swap_megabytes", "Maximum swap allocated to server in megabytes", label_names)
max_disk = Gauge("pterodactyl_server_max_disk_megabytes", "Maximum disk space allocated to server in megabytes", label_names)
io = Gauge("pterodactyl_server_io", "IO weight of server", label_names)
max_cpu = Gauge("pterodactyl_server_max_cpu_absolute", "Maximum cpu load allowed to server", label_names)


def init_metrics():
    start_http_server(9531)


def serve_metrics(metrics):
    for x in range(len(metrics["id"])):
        srv_label = metrics['name'][x]
        id_label = metrics['id'][x]
        memory.labels(srv_label, id_label).set(metrics["memory"][x])
        cpu.labels(srv_label, id_label).set(metrics["cpu"][x])
        disk.labels(srv_label, id_label).set(metrics["disk"][x])
        rx.labels(srv_label, id_label).set(metrics["rx"][x])
        tx.labels(srv_label, id_label).set(metrics["tx"][x])
        uptime.labels(srv_label, id_label).set(metrics["uptime"][x])
        max_memory.labels(srv_label, id_label).set(metrics["max_memory"][x])
        max_swap.labels(srv_label, id_label).set(metrics["max_swap"][x])
        max_disk.labels(srv_label, id_label).set(metrics["max_disk"][x])
        io.labels(srv_label, id_label).set(metrics["io"][x])
        max_cpu.labels(srv_label, id_label).set(metrics["max_cpu"][x])