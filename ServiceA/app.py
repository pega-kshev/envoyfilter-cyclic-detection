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
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    hopcount = int(request.headers.get('hopcount', 0))

    # Increment hop count
    hopcount += 1

    if hopcount > MAX_HOPS:
        return jsonify(error="Max hop count reached"), 400

    headers = {
        'x-b3-traceid': trace_id,
        'hopcount': str(hopcount)
    }

    try:
        response = requests.get(service_b_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling ServiceB: {e}")
        return jsonify(error="ServiceB call failed"), 500

    return f"ServiceA called ServiceB with trace ID: {trace_id}\nResponse from ServiceB: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)