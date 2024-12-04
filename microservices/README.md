# Setting Up NGINX on Ubuntu

This guide provides steps to install and configure NGINX on an Ubuntu system to serve your applications.

## Steps

1. **Install NGINX**:
   sudo apt update
   sudo apt install nginx -y

2. **Start and Enable NGINX**:
   sudo systemctl start nginx
   sudo systemctl enable nginx

3. **Check NGINX Status**:
   sudo systemctl status nginx

4. **Adjust Firewall (if applicable)**:
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   sudo ufw status

5. **Access NGINX Default Page**:
   Open a web browser and navigate to your server’s IP address or `http://localhost`.

6. **Configure NGINX for Your Application**:
   1. Create a new server block:
      sudo nano /etc/nginx/sites-available/myapp
   2. Add the following configuration:
      server {
          listen 80;
          server_name your_domain.com www.your_domain.com;

          location / {
              proxy_pass http://127.0.0.1:5000; # Flask app
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
      }
   3. Enable the configuration:
      sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
   4. Test the configuration:
      sudo nginx -t
   5. Restart NGINX:
      sudo systemctl restart nginx

7. **Optional: Secure NGINX with SSL**:
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your_domain.com -d www.your_domain.com

This will automatically configure HTTPS for your server.
