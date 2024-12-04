# Microservices with API Gateway
## Steps involved
#### 1. Start payments api on port 8000
#### 2. Start users api on port 8001
#### 3. Install Nginx
#### 4. Configure routing
#### 5. Launch Nginx
#### 6. Try in Postman

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

   
### Access NGINX Default Page**:
   Open a web browser and navigate to your server’s IP address or `http://localhost`.

### Configure NGINX for Your Application:
   1. Create a new server block:
      ```bash
      sudo nano /etc/nginx/sites-available/payments
      ```
   3. Add the following configuration:
      ```json
      server {
         listen 80;
         server_name 127.0.0.1;  # Replace with your actual domain or IP
      
         location  /payments  {
            proxy_pass http://127.0.0.1:8000;
         }
         
         location  /user  {
            proxy_pass http://127.0.0.1:8001;
         }
      }
      ```
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

#### Uninstalling nginx
```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
sudo apt remove --purge nginx nginx-common -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/nginx
sudo rm -rf /var/log/nginx
nginx -v
```
