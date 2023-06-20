from kafka import KafkaConsumer
from kafka import TopicPartition
import threading

TOPIC = 'persons'
CONSUMER_GROUP = 'udacity'
PARTITION = 0

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],     enable_auto_commit=True,
    consumer_timeout_ms=1000,
    auto_offset_reset='earliest')



#consumer.poll()

def consume(consumer, topics):    
    tp = TopicPartition(TOPIC, 0)
    consumer.assign([tp])
    #consumer.seek_to_beginning()

    consumer.poll()

    # read all messages and keep latest
    latest_message = list(consumer)
    for l in latest_message:
        print(l.value.decode('UTF-8'))

    consumer.close()

if __name__ == '__main__':
    consume(consumer, TOPIC)
