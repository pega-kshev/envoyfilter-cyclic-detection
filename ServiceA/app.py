from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def call_serviceB():
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    headers = {'x-b3-traceid': trace_id}
    
    # Log the outgoing request
    logging.info(f"ServiceA: Calling ServiceB with trace ID: {trace_id}")
    
    response = requests.get('http://serviceb:8080', headers=headers)
    
    # Log the response from ServiceB
    logging.info(f"ServiceA: Received response from ServiceB: {response.text}")
    
    return f"ServiceA called ServiceB with trace ID: {trace_id}\nResponse from ServiceB: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
