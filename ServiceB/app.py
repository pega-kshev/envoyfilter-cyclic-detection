from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    trace_id = request.headers.get('x-b3-traceid', 'default-trace-id')
    return f"ServiceB received trace ID: {trace_id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
