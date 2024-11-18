## Steps to enabled HTTPS communication

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
