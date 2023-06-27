from kafka import KafkaConsumer
from kafka import TopicPartition
import csv
import logging

TOPIC_P = 'persons'
TOPIC_L = 'locations'
f = 'udacity'
PARTITION = 0
KAFKA_SERVER = 'kafka-headless:9092'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")

consumer = KafkaConsumer(bootstrap_servers=[KAFKA_SERVER], enable_auto_commit=True,
                        consumer_timeout_ms=1000, auto_offset_reset='earliest', group_id='person')


class ConsumerPersons:
    @staticmethod
    def get_all_persons():
        
        logger.info("HIIIII!!!!")
        #persons_dic_lst = consume(consumer, TOPIC_P)
        logger.info("Just a little TEST")

        tp = TopicPartition(TOPIC_P, 0)
        consumer.assign([tp])
        #consumer.seekToBeginning(PARTITION)


        entities_v = []
        logger.info("About to get message_location")
        for message_p in consumer:
            p_val = message_p.value.decode('UTF-8').strip('\"')
            entities_v.append(p_val)
            logger.info("p_val is")
            logger.info(p_val)

        #remove duplicates
        set(entities_v)
        list(entities_v)


        logger.info("About to poll")
        #consumer.poll(12000)
        logger.info("I have polled")
        #raw_entities = list(consumer)
        #entities_v = [(r.value.decode('UTF-8').strip('\"')) for r in consumer]
        for v in entities_v:
            logger.info("Da VEEEE is")
            logger.info(v)
        headers = entities_v[0]
        values = entities_v[1:]
        persons_dic_lst = []

        for val in values:
            entities_dict = {}
            for (v,h) in zip(val.split(", "), headers.split(", ")):
                entities_dict[h] = v
            persons_dic_lst.append(entities_dict)

        for p in persons_dic_lst:
            logger.info(f'p id is')
            logger.info("p.values is ")
            logger.info(p.values())
            logger.info('p.keys == ')
            logger.info(p.keys())


        return persons_dic_lst

class ConsumerLocations:
    @staticmethod
    def get_all_locations():
        persons_dic_lst = consume(consumer, TOPIC_L)

        return persons_dic_lst

def consume(consumer, topic):    
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])
    consumer.poll(120000)
    raw_entities = list(consumer)


    #consumer.seek_to_beginning()

    #msg = consumer.poll()
    #print (msg.keys())
    
    #logger.info("It's comming")
    #for message in consumer:
    #    logger.info(message.value.decode('UTF-8'))


    entities_v = [(r.value.decode('UTF-8').strip('\"')) for r in raw_entities]
    logger.info(f'len(entities_v) is {len(entities_v)}')
    logger.info("YUUP!")
    print(f'len(entities_v) is {len(entities_v)}')
    headers = entities_v[0]
    values = entities_v[1:]
    entities_dic_lst = []

    for val in values:
        entities_dict = {}
        for (v,h) in zip(val.split(", "), headers.split(", ")):
            entities_dict[h] = v
        entities_dic_lst.append(entities_dict)

    return entities_dic_lst


if __name__ == '__main__':
    #persons = ConsumerPersons.get_all_persons()
    #persons = ConsumerLocations.get_all_locations()
    for p in persons:
        print(f'p id is')
        print(p['id'])
        print(p.values())
        print('p.keys == ')
        print(p.keys())
 

