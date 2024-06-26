# Overall Setup



## Python Installation

Check if python is installed

```bash
python3
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
If you see message like above, Python is installed and we are good. If not, use the following section to install Python
## Python

```bash
sudo apt update
sudo apt -y upgrade
sudo apt install python3
sudo apt install -y python3-pip
sudo apt install -y python3-venv
```

## Create a working directory
```bash
cd ~
mkdir -p dev_box/rest_api/rest_api_env
cd dev_box/rest_api/rest_api_env
python -m venv ~/dev_box/rest_api/rest_api_env
source bin/activate
```

## Install Flask
```bash
pip install Flask
pip install dicttoxml
```

## Run program
```bash
python app.py
```
