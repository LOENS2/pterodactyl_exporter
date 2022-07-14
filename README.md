# pterodactyl_exporter

### DISCLAIMER: This data target is not offical. It is still WIP and might be buggy!

A python script that exports performance metrics from Pterodactyl Panel 1.x via the Client API, converts the data to the correct format and provides a prometheus target.

This can be used for time series monitoring of Pterodactyl game servers and visualization with Grafana.

Feel free to try this script and submit an issue if needed.

To install a dev build use pip:
```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pterodactyl-exporter
```

To get the Grafana dashboard, import id `16575`.

(c) LOENS2 2022
