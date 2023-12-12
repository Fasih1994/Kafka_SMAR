import sys
import time
import json
import argparse
from confluent_kafka import (
    Consumer,
    KafkaError,
    KafkaException)


parser = argparse.ArgumentParser(
                    prog='Kafka Conumer',
                    description='Takes keyword from given topic and start pipeline')

parser.add_argument('-cn', '--consumer-number', type=int, required=True)
parser.add_argument('-t', '--topic', type=str, required=True,
                    help="Topic name to take keywords from")
parser.add_argument('-b', '--broker', type=str, required=True,
                    help='Kafka broker to listen from')
parser.add_argument('-g', '--group', type=str, required=True,
                    help='Consumer group')


def msg_process(msg):
    # time.sleep(0.8)
    print(str(msg.value().decode('utf-8')))
    # msg_str = msg.value().decode('utf-8')
    # print(json.loads(msg_str))


running = True

def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=2.1)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                consumer.commit(asynchronous=False)
                msg_process(msg)

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__=="__main__":
    args = parser.parse_args()
    print(args.topic, args.broker, args.group)
    conf = {
        'bootstrap.servers': args.broker,
        'group.id': args.group,
        'auto.offset.reset': 'smallest'}

    print(f'Starting consumer # {args.topic}')
    consumer = Consumer(conf)

    consume_loop(consumer=consumer, topics=[args.topic])