FROM python:3.9-slim
COPY ./app /app 
RUN pip3 install -r /app/requirements.txt

WORKDIR /app

EXPOSE 9089 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9089"]
