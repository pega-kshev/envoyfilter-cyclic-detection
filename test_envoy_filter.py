import requests

# Define the base URL for ServiceA
base_url = 'http://servicea:8080'

# Number of requests to send
num_requests = 15

# Headers to simulate trace information
headers = {
    'x-b3-traceid': 'test-trace-id',
    'x-b3-spanid': 'test-span-id',
    'x-b3-parentspanid': 'test-parent-span-id',
    'x-b3-sampled': '1',
    'x-b3-flags': '0',
    'hopcount': '0'
}

# Function to send requests and check responses
def send_requests():
    for i in range(num_requests):
        response = requests.get(base_url, headers=headers)
        print(f"Request {i+1}: Status Code {response.status_code}")
        if response.status_code == 429:
            print("Received HTTP 429: Too Many Requests")
            break
        else:
            print("Response:", response.text)

# Test normal behavior
print("Testing normal behavior:")
send_requests()

# Test caching behavior by changing trace ID
print("\nTesting caching behavior with different trace IDs:")
headers['x-b3-traceid'] = 'different-trace-id'
send_requests()

# Test hop count limit
print("\nTesting hop count limit:")
headers['hopcount'] = '51'
response = requests.get(base_url, headers=headers)
print(f"Hop count test: Status Code {response.status_code}")
print("Response:", response.text)

# Reset hop count for further tests
headers['hopcount'] = '0'

# Test rapid repeated requests to trigger rate limiting
print("\nTesting rate limiting with rapid requests:")
for i in range(num_requests):
    response = requests.get(base_url, headers=headers)
    print(f"Rapid Request {i+1}: Status Code {response.status_code}")
    if response.status_code == 429:
        print("Received HTTP 429: Too Many Requests")
        break
    else:
        print("Response:", response.text)