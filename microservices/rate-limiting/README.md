## Rate Limiting Using Nginx

#### Add the following line in `/etc/nginx/nginx.conf` inside `http` directive
```bash
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/m;
```

#### Create new config in /etc/nginx/sites-available
```bash
  GNU nano 6.2                                                                         payments_rate_limit

   server {
      listen 80;
      server_name 127.0.0.1;

      location  /payments  {
         limit_req zone=api_limit burst=5 nodelay;
         proxy_pass http://127.0.0.1:8000;
      }

      location  /users  {
         proxy_pass http://127.0.0.1:8001;
      }
   }
```

#### Explanation
burst=5 allows traffic bursts.
If we put the rate as 120 r/m it means nginx will set a rate of 120/60=2 req/sec. So 3rd req in single second is rejected.
Instead, we want to allow the bursts as long as overall no. of request is less than 120 in a minute
