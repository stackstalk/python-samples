#!/usr/bin/env python3

import json
from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroConsumer
from confluent_kafka import avro


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % msg.value().decode('utf-8'), str(err))
    else:
        print("Message produced: %s" % msg.value().decode('utf-8'))


def load_avro_schema_from_file():

    key_schema = avro.load("avro/movie-topic-key.avsc")
    value_schema = avro.load("avro/movie-topic-value.avsc")

    return key_schema, value_schema


def read_data():

    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "group.id": "my-connsumer1",
        "auto.offset.reset": "earliest"
    }

    #print(key_schema)
    #print(value_schema)

    consumer = AvroConsumer(consumer_config)
    consumer.subscribe(['movie-topic'])

    while True:
      try:
        msg = consumer.poll(1)

        if msg is None:
          continue

        print("Key is :" + json.dumps(msg.key()))
        print("Value is :" + json.dumps(msg.value()))
        print("-------------------------")

      except KafkaException as e:
        print('Kafka failure ' + e)

    consumer.close()

def main():
    read_data()


if __name__ == "__main__":
    main()
