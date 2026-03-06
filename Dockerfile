FROM w4bo/python:1.0.7
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /home