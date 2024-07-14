import requests
import time
# Define the URL of the endpoint

url = "http://127.0.0.1:5000/"

while (True):
    time.sleep(1.0)
    # making un-authorized access
    #response = requests.get(url)

    # making authrized access
    response = requests.get(url, auth=('john', 'hello'))

    # Print the response content
    print(response.text)
