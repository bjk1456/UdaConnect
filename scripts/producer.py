from kafka import KafkaProducer
import json
import csv


TOPIC_P = 'persons'
TOPIC_L = 'locations'
KAFKA_SERVER = 'localhost:9092'
PARTITION = 0
CONSUMER_GROUP = 'udacity'
PERSON_CSV = '../db/person.csv'
LOCATION_CSV = '../db/location.csv'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def on_send_success(record_metadata):
    print("HELLO!")
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print('I am an errback', exc_info=excp)


def producer(file, topic):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    rows = []
    with open(file) as f:
        for row in f:
            print(f'the row is {row.strip()}')
            rows.append(row.strip())
    producer.send(topic=topic, value=rows, partition=PARTITION).add_callback(on_send_success).add_errback(on_send_error)

    producer.flush()

    producer.close(timeout=5)

if __name__ == '__main__':
    for topic, file in zip([TOPIC_P, TOPIC_L], [PERSON_CSV, LOCATION_CSV]):
        print(f'topic is {topic} file is {file}') 
        producer(file, topic)
