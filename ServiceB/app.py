from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def call_serviceA():
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    headers = {'x-b3-traceid': trace_id}
    
    # Log the outgoing request
    logging.info(f"ServiceB: Calling ServiceA with trace ID: {trace_id}")
    
    response = requests.get('http://servicea:8080', headers=headers)
    
    # Log the response from ServiceA
    logging.info(f"ServiceB: Received response from ServiceA: {response.text}")
    
    return f"ServiceB called ServiceA with trace ID: {trace_id}\nResponse from ServiceA: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
