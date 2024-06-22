# Installing Prism

Steps to install Prism

## NodeJS Installation

Prism needs nodeJS. Install nodeJS using

```bash
sudo apt update
sudo apt install nodejs
```

## Install Prism

```bash
npm install -global @stoplight/prism-cli
```

## Start Mock Server By

```bash
prism mock /path/of/your/oas.yaml -p 8080
```
