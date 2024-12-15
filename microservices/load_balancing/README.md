# Distributing Traffic To Our Payments API

## Payments Microservices
### Deploy Payments API 3 times with different ports
#### Payments API 1
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 8000, debug=True)
```
Start Payments API 1
```bash
python payment1.py
```

#### Payments API 2
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 8001, debug=True)
```
Start Payments API 2
```bash
python payment2.py
```

#### Payments API 3
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 8002, debug=True)
```
Start Payments API 3
```bash
python payment3.py
```


## Users Microservices
### Deploy Users API 3 times with different ports
#### Users API 1
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 9000, debug=True)
```
Start Users API 1
```bash
python users1.py
```

#### Users API 2
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 9001, debug=True)
```
Start Users API 1
```bash
python users2.py
```

#### Users API 1
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 9002, debug=True)
```
Start Users API 1
```bash
python users3.py
```

## NGINX
#### Create a new NGINX config
```bash
sudo nano /etc/nginx/site-available/upi_load_balancing
```

Paste the following content
```javascript
upstream payments_nodes {
   server 127.0.0.1:8001;
   server 127.0.0.1:8002;
   server 127.0.0.1:8003;
}

upstream users_nodes {
   server 127.0.0.1:9000;
   server 127.0.0.1:9001;
   server 127.0.0.1:9002;
}
server {
   listen 80;
   server_name 127.0.0.1;  # Replace with your actual domain or IP

      location /payments {
         proxy_pass http://payments_nodes;
      }

      location /user {
         proxy_pass http://users_nodes;
      }
}
```

#### Test new NGINX config
```bash
nginx -t
```

#### Create link to site-enabled
```bash
sudo ln -s /etc/nginx/sites-available/upi_load_balancing /etc/nginx/sites-enabled/
```

## Also Try
#### Shutdown any one API
* Send some requests
* You will see that NGINX does not route any request to the failed server
* Eventually none of your request actually fails
* It just gets re-routed to other available servers
#### Restart NGINX
```bash
sudo systemctl restart nginx
```
