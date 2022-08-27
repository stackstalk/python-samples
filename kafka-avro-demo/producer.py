#!/usr/bin/env python3

import json
from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroProducer
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


def send_data():

    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081"
    }

    key_schema, value_schema = load_avro_schema_from_file()

    #print(key_schema)
    #print(value_schema)

    try:
        producer = AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)

        f1 = open("data/movie-metadata.json", "r")
        key_str = f1.read();
        f1.close()

        f2 = open("data/movie-details.json", "r")
        value_str = f2.read()
        f2.close()

        producer.produce(topic = "movie-topic", key = json.loads(key_str), headers = [("my-header1", "Value1")], value = json.loads(value_str))
        producer.flush()

    except KafkaException as e:
        print('Kafka failure ' + e)



def main():
    send_data()


if __name__ == "__main__":
    main()
