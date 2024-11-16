## Load Testing With Locust

#### Step 1: Installation
```bash
pip install locust
```

#### Step 2: Download the locustfile.py in your directory
#### Step 3: Keep your Payment API running on 127.0.0.1:5000
#### Step 4: Launch your locust testing file
```bash
locust -f locustfile.py --host=http://127.0.0.1:5000 --web-host=127.0.0.1 --web-port=8080
```

#### Step 5: Visit Locust UI
```bash
http://127.0.0.1:8080
```
