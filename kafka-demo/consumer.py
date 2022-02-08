from confluent_kafka import Consumer

consumer = Consumer({'bootstrap.servers': "localhost:9092",
                     'group.id': "mygroup"})

try:
    consumer.subscribe(["topic_1"])

    while True:

        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        msg_val = msg.value().decode('utf-8')
        print(msg_val)
finally:
    consumer.close()

