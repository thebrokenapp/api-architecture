import requests

# Define the URL of the endpoint
url = "http://127.0.0.1:5000/data"

# Define the headers, including content-type application/json
headers = {
    "Content-Type": "application/xml"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Print the response content
print(response.text)
