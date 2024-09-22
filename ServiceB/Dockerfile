FROM python:3.8-slim
WORKDIR /app
COPY ./ServiceB/app.py .
RUN pip install flask requests
CMD ["python", "app.py"]
