## Load Testing With Locust

#### Installation
```bash
pip install locust
```

#### Download the locustfile.py in your directory
#### Keep your Payment API running on 127.0.0.1:5000
#### Launch your locust testing file
```bash
locust -f locustfile.py --host=http://127.0.0.1:5000 --web-host=127.0.0.1 --web-port=8080
```

#### Visit Locust UI
```bash
http://127.0.0.1:8080
```
