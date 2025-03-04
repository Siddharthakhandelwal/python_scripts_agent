import requests
headers = {
        'Content-Type': 'application/json',
    }
data ={
    "name":"Sidd",
    "number":"+917300608902"
}
requests.post("https://python-scripts-agent-2.onrender.com/doctor",headers,json=data)
