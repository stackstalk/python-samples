from confluent_kafka import Producer, KafkaException


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % msg.value().decode('utf-8'), str(err))
    else:
        print("Message produced: %s" % msg.value().decode('utf-8'))


try:
    producer = Producer({'bootstrap.servers': "localhost:9092"})
    producer.produce("topic_1", "This is my async test message", callback=acked)
    producer.poll(1)

except KafkaException as e:
    print('Kafka failure ' + e)

