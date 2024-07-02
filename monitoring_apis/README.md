# API Monitoring Using Prometheus and Grafana

Installation steps using  other github repo

## Install Python Libraries

Install prometheus library 

```bash
pip install prometheus-fastapi-instrumentator
```

## Add Exposition

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(debug=True)
Instrumentator().instrument(app).expose(app)
```

## Start Your App As Usual
```bash
 uvicorn orders.app:app --reload
```

## Prepare Your Prometheus YAML File as Below
```yaml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "api-monitoring"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["127.0.0.1:8000"]
```

## Start Prometheus
```bash
 ./prometheus --web.listen-address=127.0.0.1:9001
```

## Metrics Are Available At
```bash
 http://127.0.0.1:8000/metrics
```

## Prometheus is Available At
```bash
 http://127.0.0.1:9001/
```
