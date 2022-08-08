# Pterodactyl Exporter

### Please use the Discussion for Support rather than the Issues.

A python script that exports performance metrics from Pterodactyl Panel 1.x via the Client API, converts the data to the correct format and provides a prometheus target.

This can be used for time series monitoring of Pterodactyl game servers and visualization with Grafana.

Feel free to try this script and submit an issue if needed.

## How to install

#### What you need:

 * Linux server (should run on Windows aswell, but is only tested in a linux environment)
 * Prometheus
 * Python (3.10)
 * Pterodactyl client API key (service account with read only is recommended)

#### Installed as user "prometheus":

 - To install a dev build use pip (a release and non-dev version will follow soon):
```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pterodactyl-exporter
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

 - To get the Grafana dashboard, import id `16575`. Alternatively download the JSON file from the releases (coming soon).
 
 #### To show and hide servers from being monitored, just remove the read permission of the service account on that Server

##

&copy; LOENS2 2022
