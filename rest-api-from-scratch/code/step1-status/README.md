
# Code Setup and Walkthrough

#### Create a folder 
```bash
md rest-api-from-scratch
```

#### Check if python is installed
```python
python
Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

#### Check if pip is installed
``` bash
pip -V
pip 24.0 from C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.1264.0_x64__qbz5n2kfra8p0\Lib\site-packages\pip (python 3.12)
```

#### Create a folder inside your current folder and go inside the folder
```bash
md rest-api-env
cd rest-api-env
```

#### Create virtualenv
```bash
python -m vevn <complete path to your rest-api-env folder>
```

#### Activate virtualenv
```bash
Scripts\active
```

#### Install Flask
``` bash
pip install Flask
```


# Code
Inside your folder rest-api-from-scratch create a python file: `app.py`

### First line of your code:
Import Flask library
```python
from flask import Flask
```

### Create an app object
```python
from flask import Flask

app = Flask(__name__)
```

### Add Your first route
Generally, we add a `/status` route with a `GET` request method so that if a consumer needs to find out if the API is running or not - they can just open the route in a web-browser and see the response

```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
```

Every route need to have a funtion attached to it, that will
define the code we want to execute if someone makes a request to that route.

### Add the function
Note: the name of the function can be anything, in this case we have chosen `status`
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
```

### Add the business logic for /apiStatus
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}
```

#### Add the host and port details where the API will run
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
```

#### Run the code 
```
python app.py
```
If you see soemthing like the following, the API is running successfully

```bash
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 508-625-283
```


## Try to Make the API Call

#### Check API Status From Your Browser

```http
  GET /apiStatus
  http://127.0.0.1:5000/apiStatus
```

