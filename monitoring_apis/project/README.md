
## Monitoring APIs

#### 1. Create a folder `monitoring-api`

#### 2. Download sample API code and name the file `app.py`

#### 3. Download sample python code to generate mock traffic `generate_events.py`

#### 4. Activate the previous virtual-env and after that install:
```bash
  pip install flask
  pip install prometheus-flask-exporter
```
#### Start the API
```bash
  python app.py
```

#### Start the Mock Events app:
```bash
python generate_events.py
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
.\prometheus.exe
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

Launch grafana using cmd:
```bash
.\bin\grafana-server.exe
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

