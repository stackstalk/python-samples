from confluent_kafka import Producer, KafkaException


try:
    producer = Producer({'bootstrap.servers': "localhost:9092"})
    producer.produce("topic_1", "This is my test message")
    producer.flush()

except KafkaException as e:
    print("Kafka failure " + e)
