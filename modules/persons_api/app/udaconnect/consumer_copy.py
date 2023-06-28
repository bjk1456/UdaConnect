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
    logger.info("About to get message_location")
    for message_p in consumer:
        p_val = message_p.value.decode('UTF-8').strip('\"')
        raw_entities.append(p_val)
        logger.info("test_v is")
        logger.info(raw_entities)

    consumer.poll()


    #raw_entities = list(consumer)

    #remove duplicates
    set(raw_entities)
    list(raw_entities)


    #entities_v = [(r.value.decode('UTF-8').strip('\"')) for r in raw_entities]
    logger.info(f"The len before pop is ... {len(raw_entities)}")
    headers = raw_entities.pop(0)
    logger.info(f"The len after pop is ... {len(raw_entities)}")
    #values = entities_v.pop()
    entities_dic_lst = []

    for v in raw_entities:
        logging.info("The v is ")
        logging.info(v)

    logging.info("THe headers are")
    logging.info(headers)

    for val in raw_entities:
        logging.info("The val is ")
        logging.info(val)
        entities_dict = {}
        for (v,h) in zip(val.split(", "), headers.split(", ")):
            entities_dict[h] = v
        entities_dic_lst.append(entities_dict)

    return entities_dic_lst