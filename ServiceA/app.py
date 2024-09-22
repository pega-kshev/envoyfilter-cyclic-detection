from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def call_serviceB():
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    headers = {'x-b3-traceid': trace_id}
    response = requests.get('http://serviceb:8080', headers=headers)
    return f"ServiceA called ServiceB with trace ID: {trace_id}\nResponse from ServiceB: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
