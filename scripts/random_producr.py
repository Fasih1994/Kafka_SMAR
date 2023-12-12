from confluent_kafka import Producer
import socket
import time
import argparse
import random

parser = argparse.ArgumentParser(
                    prog='Kafka ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',
                    description='Takes keyword from given topic and start pipeline')

parser.add_argument('-t', '--topic', type=str, required=True,
                    help="Topic name to send msg to")

broker = 'localhost:9093,localhost:9094,localhost:9095'

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value().decode('utf-8'))))

conf = {'bootstrap.servers': broker,
        'client.id': socket.gethostname()}

def send_msg(topic, key, msg):


    producer = Producer(conf)

    producer.produce(topic, key=str(key), value=msg, callback=acked)

    producer.poll(2)



if __name__ == "__main__":
    args = parser.parse_args()
    print(args.topic)

    for i in range(1, 10000):
        send_msg(
            topic=args.topic,
            key=random.randint(1,10000),
            msg=f"message # {i*3}")
        # if i%100 == 0:
        #     Producer(conf).flush(1)
        #     time.sleep(0.5)