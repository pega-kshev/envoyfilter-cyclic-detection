from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the maximum number of hops
MAX_HOPS = 50

# Get Service A URL from environment variable
service_a_url = os.getenv('SERVICE_A_URL', 'http://servicea:8080')

@app.route('/')
def call_serviceA():
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
        response = requests.get(service_a_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling ServiceA: {e}")
        return jsonify(error="ServiceA call failed"), 500

    return f"ServiceB called ServiceA with trace ID: {trace_id}\nResponse from ServiceA: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)