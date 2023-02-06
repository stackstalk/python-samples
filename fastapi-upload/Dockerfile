FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY app.py /app 
RUN mkdir -p /app/resources && mkdir -p /app/filecache

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8091"]
