import requests
import time
# Define the URL of the endpoint
url = "http://127.0.0.1:5000/apiStatus"
# Make the GET request
while (True):
    time.sleep(1)
    response = requests.get(url)

    # Print the response content
    print(response.text)
