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

#producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)#, group_id=CONSUMER_GROUP)

producer.send(TOPIC_P, b'Test Message!!!')
producer.flush()


def producer(file, topic):
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    with open(file) as f:
        for row in f:
            print(f'the row is {row.strip()}')
            producer.send(topic=topic, value=row.strip(), partition=PARTITION)
        producer.flush()

if __name__ == '__main__':
    for topic, file in zip([TOPIC_P, TOPIC_L], [PERSON_CSV, LOCATION_CSV]):
        print(f'topic is {topic} file is {file}') 
        producer(file, topic)
