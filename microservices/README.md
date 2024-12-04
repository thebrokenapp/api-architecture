# Setting Up NGINX on Ubuntu

This guide provides steps to install and configure NGINX on an Ubuntu system to serve your applications.

## Steps
**Install NGINX**:
   ```bash
   sudo apt update
   sudo apt install nginx -y
   ```
**Start and Enable NGINX**:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

**Check NGINX Status**:
   ```bash
   sudo systemctl status nginx
   ```
**Adjust Firewall (if applicable)**:
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   sudo ufw status
   ```

   
**Access NGINX Default Page**:
   Open a web browser and navigate to your server’s IP address or `http://localhost`.

**Configure NGINX for Your Application**:
   1. Create a new server block:
      ```bash
      sudo nano /etc/nginx/sites-available/myapp
      ```
   3. Add the following configuration:
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
   4. Enable the configuration:
      ```bash
      sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
      ```
   5. Test the configuration:
      ```bash
      sudo nginx -t
      ```
   7. Restart NGINX:
      ```bash
      sudo systemctl restart nginx
      ```

