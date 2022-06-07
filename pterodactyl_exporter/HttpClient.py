import http.client
import json
from os import environ

client = None
headers = None
srv = None


def client_init():
    global client
    global headers
    if environ['HTTPS']:
        client = http.client.HTTPSConnection(environ['HOST'], 443)
    else:
        client = http.client.HTTPConnection(environ['HOST'], 80)
    headers = {"Authorization": f"Bearer {environ['API_KEY']}", "Content-Type": "application/json",
               "Accept": "Application/vnd.pterodactyl.v1+json"}


def get_server():
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
        "max_swap" :[],
        "max_disk": [],
        "io": [],
        "max_cpu": []
    }
    client.request("GET", "/api/client/", "", headers)
    servers = json.loads(client.getresponse().read())
    print(servers)
    for x in servers['data']:
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
        metrics = json.loads(client.getresponse().read())["attributes"]['resources']
        srv["memory"].append(metrics["memory_bytes"]/106496)
        srv["cpu"].append(metrics["cpu_absolute"])
        srv["disk"].append(metrics["disk_bytes"]/106496)
        srv["rx"].append(metrics["network_rx_bytes"]/106496)
        srv["tx"].append(metrics["network_tx_bytes"]/106496)
        srv["uptime"].append(metrics["uptime"])
    return srv
