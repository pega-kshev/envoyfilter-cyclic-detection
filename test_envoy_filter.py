import requests

# Define the base URL for ServiceA
base_url = 'http://servicea:8080'

# Number of requests to send
num_requests = 10

# Headers to simulate trace information
headers = {
    'x-b3-traceid': 'test-trace-id',
    'x-b3-spanid': 'test-span-id',
    'x-b3-parentspanid': 'test-parent-span-id',
    'x-b3-sampled': '1',
    'x-b3-flags': '0',
    'hopcount': '0'
}

# Send requests and check responses
for i in range(num_requests):
    response = requests.get(base_url, headers=headers)
    print(f"Request {i+1}: Status Code {response.status_code}")
    if response.status_code == 429:
        print("Received HTTP 429: Too Many Requests")
        break
    else:
        print("Response:", response.text)