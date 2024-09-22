# envoyfilter-cyclic-detection
EnvoyFilter solution to detect cyclic HTTP requests

# EnvoyFilter Cyclic Detection

This project demonstrates using EnvoyFilter to detect cyclic HTTP requests.

## Setup

- **Helm:** `helm upgrade --install my-test-services ./test-services`
- **EnvoyFilter:** Apply with `kubectl apply -f envoyfilter.yaml`

## Running Tests

Execute JMeter tests using `test_plan.jmx` to simulate cyclic requests.
