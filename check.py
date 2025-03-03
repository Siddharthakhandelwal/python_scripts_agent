import requests

url = "https://python-scripts-agent-1.onrender.com/make-call"
data = {
    "name": "John Doe",
    "number": "+917300608902",
    
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
