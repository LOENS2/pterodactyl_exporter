import http.client
import json
import time
import dateutil.parser

client = None
headers = None
srv = None


def client_init(config_file: dict):
    global client
    global headers
    if config_file['https']:
        client = http.client.HTTPSConnection(config_file['host'], 443, check_hostname=not config_file['ignore_ssl'])
    else:
        client = http.client.HTTPConnection(config_file['host'], 80)
    headers = {"Authorization": f"Bearer {config_file['api_key']}", "Content-Type": "application/json",
               "Accept": "Application/vnd.pterodactyl.v1+json"}


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
    # if "errors" in servers:
    if not servers.status == 200:
        print(servers.read())
        time.sleep(10)
        get_server(list_type)
    for x in json.loads(servers.read())['data']:
        srv["name"].append(x['attributes']['name'])
        srv["id"].append(x['attributes']['identifier'])
        srv["max_memory"].append(x['attributes']['limits']['memory'])
        srv["max_swap"].append(x['attributes']['limits']['swap'])
        srv["max_disk"].append(x['attributes']['limits']['disk'])
        srv["io"].append(x['attributes']['limits']['io'])
        srv["max_cpu"].append(x['attributes']['limits']['cpu'])


def get_metrics():
    for x in srv["id"]:
        client.request("GET", f"/api/client/servers/{x}/resources", "", headers)
        response = client.getresponse()
        # if "errors" in response:
        if not response.status == 200:
            print(response.read())
            time.sleep(10)
            get_metrics()
        metrics = json.loads(response.read())["attributes"]['resources']
        srv["memory"].append(metrics["memory_bytes"] / 1000000)
        srv["cpu"].append(metrics["cpu_absolute"])
        srv["disk"].append(metrics["disk_bytes"] / 1000000)
        srv["rx"].append(metrics["network_rx_bytes"] / 1000000)
        srv["tx"].append(metrics["network_tx_bytes"] / 1000000)
        srv["uptime"].append(metrics["uptime"])

        get_last_backup_time(x, 1)

    return srv


def get_last_backup_time(x, page):
    client.request("GET", f"/api/client/servers/{x}/backups?per_page=50&page={page}", "", headers)
    response = json.loads(client.getresponse().read())
    if "errors" in response:
        print(response)
        time.sleep(10)
        get_metrics()
    total_pages = response['meta']['pagination']['total_pages']
    if page < total_pages:
        return get_last_backup_time(x, page + 1)

    successful_backup_times = sorted([
        dateutil.parser.isoparse(backup['attributes']['completed_at'])
        for backup in response['data']
        if backup["attributes"]["is_successful"]
    ])

    if successful_backup_times:
        srv["last_backup_time"].append(successful_backup_times[-1].timestamp())
    else:
        srv["last_backup_time"].append(0)
