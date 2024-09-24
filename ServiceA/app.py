import os
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the maximum number of hops
MAX_HOPS = 50

# Get Service B URL from environment variable
service_b_url = os.getenv('SERVICE_B_URL', 'http://serviceb:8080')

@app.route('/')
def call_serviceB():
    logging.info(f"Received request with headers: {request.headers}")
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    span_id = request.headers.get('x-b3-spanid', 'default-span-id')
    parent_span_id = request.headers.get('x-b3-parentspanid', 'default-parent-span-id')
    sampled = request.headers.get('x-b3-sampled', '1')
    flags = request.headers.get('x-b3-flags', '0')
    hopcount = int(request.headers.get('hopcount', 0))

    # Increment hop count
    hopcount += 1

    if hopcount > MAX_HOPS:
        return jsonify(error="Max hop count reached"), 400

    headers = {
        'x-b3-traceid': trace_id,
        'x-b3-spanid': span_id,
        'x-b3-parentspanid': parent_span_id,
        'x-b3-sampled': sampled,
        'x-b3-flags': flags,
        'hopcount': str(hopcount)
    }

    response_code = 500
    try:
        response = requests.get(service_b_url, headers=headers)
        response_code = response.status_code

        # Check if the response is 429 and propagate it
        if response.status_code == 429:
            return jsonify(error="Too Many Requests"), 429

        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling ServiceB: {e}")
        return jsonify(error="ServiceB call failed"), response_code

    return f"ServiceA called ServiceB with trace ID: {trace_id}\nResponse from ServiceB: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)