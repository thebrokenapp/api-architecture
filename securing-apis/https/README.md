## Steps to enabled HTTPS communication

#### Install OpenSSL
```bash
sudo apt update
sudo apt install openssl
```

#### Setup your Own CA
##### Create a directory structure for your CA 
```
mkdir -p ~/myCA/newcerts                 -> keep all the certs that are issues by CA
mkdir ~/myCA/private                     -> private cert of CA
mkdir ~/myCA/certs                       -> public cert of CA
touch ~/myCA/myCAindex                   -> needed for some internal file and cert tracking
```

##### Generate the Root(CA) Private Key
This will create a private key for your CA (myCA.key) with encryption.
You'll need to set a password for this key
Remember this password - as it will be needed everytime to sign any certificate
`-aes256` adds extra layer of password protection on CA's private key. CA private key is highly sensitive as its used to sign requestor's public key
```bash
openssl genpkey -algorithm RSA -out ~/myCA/private/myCA.key -aes256
chmod 400 ~/myCA/private/myCA.key
```

##### Create the Root(CA) Public Certificate
This will prompt you for information like country, state, organization, and common name. For common name, use something like My Local CA.
```bash
openssl req -key ~/myCA/private/myCA.key -new -x509 -out ~/myCA/certs/myCA.crt
```



#### Generate API Server Certificates
Generate a Private Key for the Server:
```bash
openssl genpkey -algorithm RSA -out server.key
chmod 400 server.key
```

Generate a CSR (Certificate Signing Request):
```bash
openssl req -new -key server.key -out server.csr
```
This will prompt you for information about your server. The Common Name (CN) should be the domain name of your server (e.g., localhost or mydomain.local for local development).

#### Sign the CSR with Your Local CA:
```bash
openssl x509 -req -in server.csr -CA ~/myCA/certs/myCA.crt -CAkey ~/myCA/private/myCA.key -CAcreateserial -out server.crt -days 365
```

This will sign the CSR with your local CA's private key and generate the server's certificate (server.crt).


#### Combine the Server Certificate and CA Certificate (Optional):
```bash
cat server.crt ~/myCA/certs/myCA.crt > server-chain.crt
```

#### Sample Python Code
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, HTTPS with Local CA!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context=('server-chain.crt', 'server.key'))
```


