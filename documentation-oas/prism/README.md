## Deploying Mock Server using OAS File

#### Download the oas.yaml file that you have created and keep it in a directory

#### Check if nodejs is installed
```bash
node -v
```

#### Install prism
```bash
npm install prism -g @stoplight/prism-cli
```


#### Start your mock server
```bash
prism mock ./oas.yaml -p 5000
```


#### Check if you are getting the response in POSTMAN
```bash
If you want to see specific examples that you have added in OAS file
Add a header=> "Prefer: example=txn_3"
```

#### You can make a request using bash too
```bash
curl -H "Content-Type: application/json" http://127.0.0.1:5000/apiStatus

curl -H "Content-Type: application/json" http://127.0.0.1:5000/payments/beatae

curl -X GET -H "Content-Type: application/json" -H "Prefer: example=txn_2" http://127.0.0.1:5000/payments/txn_2
```
