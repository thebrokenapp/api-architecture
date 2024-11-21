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






Enable HTTPS for Flask App

1. Install OpenSSL
Ensure you have OpenSSL installed on your system. It is used to generate the keys and certificates.

For Ubuntu:
	sudo apt update
	sudo apt install openssl


2. Create Your Own Local CA (One time setup)
	A Certificate Authority (CA) is used to sign and verify SSL certificates. You will create a root certificate for your local CA that will allow you to sign SSL certificates for development.

	Steps to Create a Local CA:
		a. Create a directory structure for your CA:
			mkdir -p ~/myCA/newcerts
			mkdir ~/myCA/private
			mkdir ~/myCA/certs
			touch ~/myCA/myCAindex
		b. Generate the Root Private Key: The root key will be used to sign all certificates.
			openssl genpkey -algorithm RSA -out ~/myCA/private/myCA.key -aes256
			chmod 400 ~/myCA/private/myCA.key

			This will create a private key for your CA (myCA.key) with encryption. You'll need to set a password for this key
		c. Create the Root Certificate: This certificate will serve as the trusted certificate to sign others.
			openssl req -key ~/myCA/private/myCA.key -new -x509 -out ~/myCA/certs/myCA.crt
			This will prompt you for information like country, state, organization, and common name. For common name, use something like My Local CA.

3. Generate the SSL Certificate for Your Flask API
	a. Generate a Private Key for the Server:
		openssl genpkey -algorithm RSA -out server.key
		chmod 400 server.key

	b. Generate a CSR (Certificate Signing Request):
		openssl req -new -key server.key -out server.csr

		This will prompt you for information about your server. The Common Name (CN) should be the domain name of your server (e.g., localhost or mydomain.local for local development).

4. Sign the CSR with Your Local CA:
	openssl x509 -req -in server.csr -CA ~/myCA/certs/myCA.crt -CAkey ~/myCA/private/myCA.key -CAcreateserial -out server.crt -days 365

	This will sign the CSR with your local CA's private key and generate the server's certificate (server.crt).

5. Combine the Server Certificate and CA Certificate (Optional): You can bundle the server certificate with the root CA certificate to create a certificate chain. This step is needed if the browser requires the full chain.
	cat server.crt ~/myCA/certs/myCA.crt > server-chain.crt

6. Flask Code
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, HTTPS with Local CA!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context=('server-chain.crt', 'server.key'))


















## Alternative

#### Generate a Self-Signed SSL Certificate
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

In the prompt, you can add any answers, in the common name or FQDN add 127.0.0.1
```

This will create two files for you
`key.pem`
`cert.pem`

#### Update your payments.py by changing the last line
```python
if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True, ssl_context=('./cert.pem', './key.pem'))
```
