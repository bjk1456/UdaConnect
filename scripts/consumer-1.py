from kafka import KafkaConsumer
from kafka import TopicPartition
import time

TOPIC = 'persons1'
CONSUMER_GROUP = 'udacity'
PARTITION = 0

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'], max_poll_interval_ms=9)



#consumer.poll()

def get_all_objects(topic):
    tp = TopicPartition(TOPIC, 0)
    consumer.assign([tp])
    #consumer.seek_to_beginning()
    i = 0
    print("About to poll")
    msg = consumer.poll()
    #consumer.poll()
    if msg is None: 
        print("None")
    
    
    for message in consumer:
        print (message.value.decode('UTF-8'))
        i += 1
        print(f'i == {i}')

    consumer.close()

if __name__ == '__main__':
    #persons = ConsumerPersons.get_all_persons()
    persons = get_all_objects(TOPIC)
    for p in persons:
        print(f'p id is')
        print(p['id'])
        print(p.values())
        print('p.keys == ')
        print(p.keys())
 
