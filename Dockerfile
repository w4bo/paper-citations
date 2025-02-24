FROM w4bo/python:1.0.3
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /home