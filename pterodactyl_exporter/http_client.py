import http.client
import json
import ssl
import dateutil.parser

client = None
headers = None
srv = None
MiB_TO_MB = 1.048576


def client_init(config_file: dict):
    global client
    global headers
    if config_file['https']:
        context = ssl.create_default_context()
        context.check_hostname = not config_file['ignore_ssl']
        client = http.client.HTTPSConnection(config_file['host'], 443, context=context)
    else:
        client = http.client.HTTPConnection(config_file['host'], 80)
    headers = {"Authorization": f"Bearer {config_file['api_key']}", "Content-Type": "application/json",
               "Accept": "application/json"}


def get_server(list_type="owner"):
    global srv
    srv = {
        "name": [],
        "id": [],
        "memory": [],
        "cpu": [],
        "disk": [],
        "rx": [],
        "tx": [],
        "uptime": [],
        "max_memory": [],
        "max_swap": [],
        "max_disk": [],
        "io": [],
        "max_cpu": [],
        "last_backup_time": [],
    }
    client.request("GET", "/api/client/?type={}".format(list_type), "", headers)
    servers = client.getresponse()
    if not servers.status == 200:
        raise Exception(f"Servers: \n{servers.read().decode('utf-8')}")
    for x in json.loads(servers.read())['data']:
        srv["name"].append(x['attributes']['name'])
        srv["id"].append(x['attributes']['identifier'])
        srv["max_memory"].append(x['attributes']['limits']['memory'] * MiB_TO_MB)
        srv["max_swap"].append(x['attributes']['limits']['swap'] * MiB_TO_MB)
        srv["max_disk"].append(x['attributes']['limits']['disk'] * MiB_TO_MB)
        srv["io"].append(x['attributes']['limits']['io'])
        srv["max_cpu"].append(x['attributes']['limits']['cpu'])


def get_metrics():
    for idx, x in enumerate(srv["id"]):
        client.request("GET", f"/api/client/servers/{x}/resources", "", headers)
        response = client.getresponse()
        response_read = response.read()
        if not response.status == 200:
            raise Exception(f"Fetch metrics for {srv["name"][idx]}: \n{response_read.decode('utf-8')}")
        response_dict = json.loads(response_read)
        metrics = response_dict["attributes"]['resources']
        srv["memory"].append(metrics["memory_bytes"] / 1000000)
        srv["cpu"].append(metrics["cpu_absolute"])
        srv["disk"].append(metrics["disk_bytes"] / 1000000)
        srv["rx"].append(metrics["network_rx_bytes"] / 1000000)
        srv["tx"].append(metrics["network_tx_bytes"] / 1000000)
        srv["uptime"].append(metrics["uptime"])

        get_last_backup_time(idx, x, 1)

    return srv


def get_last_backup_time(idx, x, page):
    client.request("GET", f"/api/client/servers/{x}/backups?per_page=50&page={page}", "", headers)
    response = client.getresponse()
    response_read = response.read()
    if not response.status == 200:
        raise Exception(f"Fetch last backup for {srv["name"][idx]}: \n{response_read.decode('utf-8')}")
    response_dict = json.loads(response_read)
    total_pages = response_dict['meta']['pagination']['total_pages']
    if page < total_pages:
        return get_last_backup_time(x, page + 1)

    successful_backup_times = sorted([
        dateutil.parser.isoparse(backup['attributes']['completed_at'])
        for backup in response_dict['data']
        if backup["attributes"]["is_successful"]
    ])

    if successful_backup_times:
        srv["last_backup_time"].append(successful_backup_times[-1].timestamp())
    else:
        srv["last_backup_time"].append(0)
