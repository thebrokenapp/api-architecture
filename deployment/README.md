# Deploying REST API with gunicorn

### Install gunicorn
```bash
pip install gunicorn
```

### Test your API startup with gunicorn
```bash
gunicorn --workers 3 --bind 127.0.0.1:8000 payments:app
```

Note the 3 processes that will start.
Your API is now running on `8000` ignoring the `flask-dev` server that you might have given as `5000`
Try to make some `POSTMAN` requests to see if the API is working fine or not.

### Make some changes in the logger
Since we have 3 processes running, we might want to log which request is coming to which process, etc.
To do that make the following chane in the logging logic
```python
logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [PID %(process)d] - %(message)s',
    filemode='a'
)
```
We have added the `PID` to the format so that we know which process ID is serving a request.

### Re-test your API
```bash
gunicorn --workers 3 --bind 127.0.0.1:8000 payments:app
```

Make some requests and check the `audit.log` file.
Also observer how `gunicorn` is internally managing the traffic distribution
This helps with `scalability`. Our API is much more scalable now that 3 processes are running.
But we also need to make it `durable`, where we want to ensure that if for some reason one or many process fails - it auto re-starts.
For that we will create a `service` using `systemd`

### Create a Service File
```bash
sudo nano /etc/systemd/system/payments.service
```

### Add the Configuration
```ini
[Unit]
Description=Gunicorn instance to serve payments API
After=network.target

[Service]
User=ankit
Group=ankit
WorkingDirectory=/dev_box/trainings/npci-hyd-jan-2025/trials/deployment
ExecStart=/dev_box/trainings/npci-hyd-jan-2025/api_env/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 payments:app
Restart=always
RestartSec=5
Environment="PATH=/dev_box/trainings/npci-hyd-jan-2025/api_env/bin"

[Install]
WantedBy=multi-user.target
```

### If you are not sure about your `user` or `group` details, you can find out
```bash
whoami    => this will give user name
groups    => this will give group name
id        => for other details
```


### Start and Enable Service
```bash
sudo systemctl start payments
sudo systemctl enable payments
```

### Check Service Status
```bash
sudo systemctl status payments
```

### Check logs for your service:
```bash
journalctl -u payments -f
```
Keep the logs running and try killing one process in another terminal

### Kill the service and see the effect on logs
```bash
ps ax | grep payments:app
kill -9 <pid>
```

### Try rebooting server and check if API is up after restart too


### Dependencies
```bash
pip install flask
pip install redis
pip install Flask-Pydantic
pip install pydantic
pip install prometheus-flask-exporter
pip install Flask-Limiter
pip install PyJWT
pip install PyJWT -U
pip install Flask-HTTPAuth
pip install gunicorn
```
