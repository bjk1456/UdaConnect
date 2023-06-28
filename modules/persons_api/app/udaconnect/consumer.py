from kafka import KafkaConsumer
from kafka import TopicPartition
import csv
import logging

TOPIC_P = 'persons'
TOPIC_L = 'locations'
CONSUMER_GROUP = 'udacity'
PARTITION = 0
KAFKA_SERVER = 'kafka-headless:9092'



consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER], enable_auto_commit=True,
                        consumer_timeout_ms=1000, auto_offset_reset='earliest')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

class ConsumerPersons:
    @staticmethod
    def get_all_persons():
        persons_dic_lst = consume(consumer, TOPIC_P)

        return persons_dic_lst

class ConsumerLocations:
    @staticmethod
    def get_all_locations():
        persons_dic_lst = consume(consumer, TOPIC_L)

        return persons_dic_lst

def consume(consumer, topic):    
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])

    raw_entities = []
    for message_p in consumer:
        p_val = message_p.value.decode('UTF-8').strip('\"')
        raw_entities.append(p_val)

    #remove duplicates
    set(raw_entities)
    list(raw_entities)

    headers = raw_entities.pop(0)
    entities_dic_lst = []

    for val in raw_entities:
        entities_dict = {}
        for (v,h) in zip(val.split(", "), headers.split(", ")):
            entities_dict[h] = v
        entities_dic_lst.append(entities_dict)

    return entities_dic_lst