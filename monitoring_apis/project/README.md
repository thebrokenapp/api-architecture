
## Monitoring APIs

#### Python Package Installation
```bash
  pip install prometheus-flask-exporter
```

#### Make Following changes to your Payments API
```python
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)
```

Make sure you don't have debug as `True` in the startup
```python
if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8000)
```

Check if your API is exporting metrics
```bash
Go to http://127.0.0.1:8000/metrics
```


#### Start the Mock Events app:
```bash
python payments_traffic_generator.py
OR
Start locustfile to generate load
```


#### Node Exporter
Download node-exporter
``` bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar -xvf node_exporter-1.8.2.linux-amd64.tar.gz
```

Extract node-exporter
``` bash
tar -xvf node_exporter-1.8.2.linux-amd64.tar.gz
```

Launch node-exporter
```bash
./node_exporter --web.listen-address=127.0.0.1:9100
```
Check if node-exporter is exporting the System metrics
```bash
Go to http://127.0.0.1:9100/metrics
```


### Prometheus
Download `prometheus` from the following link:

In the Operating System drop-down select `windows`
```url
https://prometheus.io/download/
```

Once the zip file is downloaded, place it in your `monitoring-api` folder and `extract` it

Inside the prometheus directory you will find a file: `prometheus.yaml`. Replace the content of the file with one from:

```url
https://raw.githubusercontent.com/thebrokenapp/api-architecture/main/monitoring_apis/project/prometheus.yaml
```

Start prometheus from command line:
```bash
.\prometheus.exe (Windows)
./prometheus --web.listen-address=127.0.0.1:9090 (Linux)
```

To check if prometheus is started correctly, go to:
```url
127.0.0.1:9090
```

### Grafana
Download `grafana` from:

In the edition select `OSS` instead of `enterprise` and in the `OS` choose `windows`
```url
https://grafana.com/grafana/download?edition=oss&platform=windows
```

Click on download `standalone binaries`

Once downloaded, place the zip file in your `monitoring-api` folder and extract it.

#### For linux
Edit your config/defaults.ini file
In the `server` section change the value of `http_addr` to represent as below
`http_addr =127.0.0.1`

Launch grafana using cmd:
```bash
.\bin\grafana-server.exe (Windows)
bin/grafana server (Linux)
```

To see if `grafana` is running properly, go to:
```url
127.0.0.1:3000
```
Credentials
```yaml
username: admin
password: admin
```
#### Add Prometheus as the data source to Grafana
* Go to Grafana Menu
* Click on Data Sources
* Add Data source
* In the URL, give the URL where Prometheus is running: `http://127.0.0.1:9090`
* Click on Save and Test

#### Server Monitoring (CPU, RAM, Disk, Network, etc)
* Click on Grafana Menu
* Dashobards -> Import
* Use the code `1860`
* Name the dashboard
* Choose data source as prometheus

#### API Dashboards
```bash
REQUESTS: (Count Based)
1. Total HTTP Requests:
	sum(flask_http_request_total)
2. Total GET Requests:
	sum(flask_http_request_total{method="GET"})
2. Total POST Requests:
	sum(flask_http_request_total{method="POST"})
2. Total PATCH Requests:
	sum(flask_http_request_total{method="PATCH"})
2. Total DELETE Requests:
	sum(flask_http_request_total{method="DELETE"})


LATENCY (Line Chart Based)
* GET ALL Payments: (flask_http_request_duration_seconds_sum{path="/payments", method="GET"}/flask_http_request_duration_seconds_count{path="/payments",method="GET"})*1000
* Make a Payment: (flask_http_request_duration_seconds_sum{path="/payments", method="POST"}/flask_http_request_duration_seconds_count{path="/payments",method="POST"})*1000
* Delete a Payment: (sum(flask_http_request_duration_seconds_sum{method="DELETE"})/sum(flask_http_request_duration_seconds_count{method="DELETE"}))*1000
* Update a payment: (sum(flask_http_request_duration_seconds_sum{method="PATCH"})/sum(flask_http_request_duration_seconds_count{method="PATCH"}))*1000


TRAFFIC (Line Chart Based)
rate(
  flask_http_request_total[30s]
)


RESPONSE CODES (Count Based)
* Success: flask_http_request_total{status="200"}
* Created: flask_http_request_total{status="201"}
* Not Found: flask_http_request_total{status="404"}
* Deleted: flask_http_request_total{status="204"}
```
### AlertManager
Download the alertmanager from
```url
wget https://github.com/prometheus/alertmanager/releases/download/v0.28.0-rc.0/alertmanager-0.28.0-rc.0.linux-amd64.tar.gz
```

Extract the content on the zip file in your `monitoring-api` folder

Enable email authorization in your personal gmail, go to:
```url
https://myaccount.google.com/apppasswords
```
Enter `name` and remember this name
You will be give a 16 digit code - copy it somewhere - if you close the window you will loose it forever


Inside the folder, replace your existing `alertmanager.yaml` with the one present here:
```url
https://github.com/thebrokenapp/api-architecture/blob/main/monitoring_apis/project/alertmanager.yaml
```
In this file change the `email addresses`, `auth-identity` and `auth-password`


Also, stop your `prometheus` and download the file
```url
https://github.com/thebrokenapp/api-architecture/blob/main/monitoring_apis/project/alert-rules.yaml
```
Place this `alert-rules.yaml` file in prometheus folder and restart prometheus

Start alert manager
```
.\alertmanager.exe (Windows)
./alertmanager --web.listen-address=127.0.0.1:9093 (Linux)
```

