from kafka import KafkaConsumer
from kafka import TopicPartition
import csv

TOPIC_P = 'persons'
TOPIC_L = 'locations'
CONSUMER_GROUP = 'udacity'
PARTITION = 0
KAFKA_SERVER = 'kafka-headless:9092'



consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER], enable_auto_commit=True,
                        consumer_timeout_ms=1000, auto_offset_reset='earliest')



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
    consumer.poll()
    raw_entities = list(consumer)
    entities_v = [(r.value.decode('UTF-8').strip('\"')) for r in raw_entities]
    headers = entities_v[0]
    values = entities_v[1:]
    entities_dic_lst = []

    for val in values:
        entities_dict = {}
        for (v,h) in zip(val.split(", "), headers.split(", ")):
            entities_dict[h] = v
        entities_dic_lst.append(entities_dict)

    return entities_dic_lst