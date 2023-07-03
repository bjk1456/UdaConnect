from kafka import KafkaProducer
import json
import csv
import logging


TOPIC_P = 'persons'
TOPIC_L = 'locations'
KAFKA_SERVER = 'kafka:9092'
PARTITION = 0
CONSUMER_GROUP = 'udacity'
PERSON_CSV = '/app/udaconnect/person.csv'
LOCATION_CSV = '/app/udaconnect/location.csv'

#producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

class ProducePersons:
    @staticmethod
    def produce_persons():
        #for topic, file in zip([TOPIC_P, TOPIC_L], [PERSON_CSV, LOCATION_CSV]):
        #    print(f'topic is {topic} file is {file}') 
        logger.info("about to produce ...")
        #producer(TOPIC_P, PERSON_CSV)
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        with open(PERSON_CSV) as f:
            for row in f:
                logger.info(f'the row is {row.strip()}')
                producer.produce(topic=TOPIC_P, value=row.strip(), partition=PARTITION, key="key1")
        #producer.flush()
       # producer.close()

    @staticmethod
    def producer(file, topic):
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        with open(file) as f:
            for row in f:
                print(f'the row is {row.strip()}')
                producer.send(topic=topic, value=row.strip(), partition=PARTITION)
        producer.flush()
        producer.close()

#if __name__ == '__main__':
#    for topic, file in zip([TOPIC_P, TOPIC_L], [PERSON_CSV, LOCATION_CSV]):
#        print(f'topic is {topic} file is {file}') 
#        producer(file, topic)
