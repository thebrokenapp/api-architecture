# Setup Instructions

## NodeJS Installation

Go to node download page [here](https://nodejs.org/en/download/prebuilt-installer) to download nodeJS msi


## Check node and npm installation
Open cmd and run:

```bash
 node -v
```
```bash
 npm -v
```
For both the commands, you should get a version number as an output like: v20.15.0
## Install http-server
```bash
 npm install -g http-server
```

## Download Swagger Editor from

[Swagger Editor](https://github.com/swagger-api/swagger-editor)

## Start Swagger Editor Server
```bash
 http-server swagger-editor-master --cors
```
