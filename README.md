# Pterodactyl Exporter

### Please use the Discussion for Support rather than the Issues.

A python script that exports performance metrics from Pterodactyl Panel 1.x via the Client API, converts the data to the correct format and provides a prometheus target.

This can be used for time series monitoring of Pterodactyl game servers and visualization with Grafana.

Feel free to try this script and submit an issue if needed.

# How to install

#### What you need:

 * Linux server (should run on Windows as well, but is only tested in a linux environment)
 * Prometheus
 * Python (3.10)
 * Pterodactyl client API key (service account with read only is recommended)

## Run as service

#### Installed as user "prometheus":

 - To install with pip:
```
pip install pterodactyl-exporter
```
 - Create directory `pterodactyl_exporter`.
 
 - Create the config file `config.yml` in that directory (set the values as needed, it's recommended to use https):
 
 ```yml
host: panel.example.com
api_key: APIKEY_APIKEYAPIKEYAPIKEY
https: true
ignore_ssl: false
 ```

 - Create systemd service `/etc/systemd/system/pterodactyl_exporter.service`:
```
[Unit]
Description=Prometheus Server
After=network-online.target

[Service]
User=prometheus
Restart=on-failure
ExecStart=pterodactyl_exporter \
--config-file=/home/prometheus/pterodactyl_exporter/config.yml

[Install]
WantedBy=multi-user.target
```

 - Enable and start the service.
 
 - Add a job configuration:
 
 ```yml
 - job_name: 'pterodactyl_exporter'
    static_configs:
      - targets: ['localhost:9531']

 ```

 - To get the Grafana dashboard, import id `16575`. Alternatively download the JSON file from the releases.
 
 #### To show and hide servers from being monitored, just remove the read permission of the service account on that Server
 
## Run with Docker

 - Create a folder named `pterodactyl_exporter`
 
 - Download the config file from GitHub:
 ```
 curl -fsSL -o config.yml https://raw.githubusercontent.com/LOENS2/pterodactyl_exporter/master/config.yml
 ```
 - Create a folder named `docker`
 
 - Download the `docker-compose.yml` into that folder:
 ```
 curl -fsSL -o docker-compose.yml https://raw.githubusercontent.com/LOENS2/pterodactyl_exporter/master/docker/docker-compose.yml
 ```
 - Run the container:
 ```
 docker-compose up -d
 ```
 
## Run manually

#### Only meant for testing purposes, not recommended for production use!

 - Clone the project:
```
git clone https://github.com/LOENS2/pterodactyl_exporter.git
```
 - Change to the clone directory
 - Run with python:
```
python -m pterodactyl_exporter.pterodactyl_exporter --config-file=config.yml
```

# Troubleshooting

You can view the output with (Time is UTC):

```
sudo journalctl -u pterodacyl_exporter.service -b --since "2024-12-14 13:45:27"
```

Post any stacktraces as an Issue.

##

With special thanks to @grimsi for helping me with docker.

&copy; LOENS2 2022
