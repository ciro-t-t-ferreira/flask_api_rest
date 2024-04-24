import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + 'video/1', {"likes":10, "name": "Flask is fun", "views": 137137})
print(response.json())
input() #that will wait for a input of the user
response = requests.get(BASE + 'video/5')
print(response.json())