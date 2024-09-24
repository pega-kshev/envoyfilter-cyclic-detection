from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the maximum number of hops
MAX_HOPS = 50

@app.route('/')
def call_serviceA():
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    span_id = request.headers.get('x-b3-spanid', 'default-span-id')
    parent_span_id = request.headers.get('x-b3-parentspanid', 'default-parent-span-id')
    sampled = request.headers.get('x-b3-sampled', '1')
    flags = request.headers.get('x-b3-flags', '0')
    hopcount = int(request.headers.get('hopcount', 0))
    
    # Increment hop count
    hopcount += 1
    
    if hopcount > MAX_HOPS:
        return f"ServiceB: Max hop count reached with trace ID: {trace_id}"
    
    headers = {
        'x-b3-traceid': trace_id,
        'x-b3-spanid': span_id,
        'x-b3-parentspanid': parent_span_id,
        'x-b3-sampled': sampled,
        'x-b3-flags': flags,
        'hopcount': str(hopcount)
    }
    
    # Log the outgoing request
    logging.info(f"ServiceB: Calling ServiceA with trace ID: {trace_id} and hopcount: {hopcount}")
    
    response = requests.get('http://servicea:8080', headers=headers)
    
    # Log the response from ServiceA
    logging.info(f"ServiceB: Received response from ServiceA: {response.text}")
    
    return f"ServiceB called ServiceA with trace ID: {trace_id}\nResponse from ServiceA: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
