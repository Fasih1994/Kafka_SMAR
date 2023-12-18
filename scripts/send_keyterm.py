import socket
import argparse
import random
import json
import os

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


parser = argparse.ArgumentParser(
                    prog='Kafka',
                    description='Takes keyword from given topic and start pipeline')


parser.add_argument('-t', '--topic', type=str, required=True,
                    help="Topic name to send msg to")


conf = {'bootstrap.servers': 'localhost:9093,localhost:9094,localhost:9095',
        'client.id': socket.gethostname(),
        'enable.idempotence': True}


MSG = {
    "user_id": None,
    "organization_id": None,
    "key_term": None,
    "platform": None,
    # "kwargs": {}
}


schema = 'keyterm.avsc'
path = os.path.realpath(os.path.dirname(__file__))
with open(f"{path}/schema/avro/{schema}") as f:
    schema_str = f.read()

schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(schema_registry_client,
                                    schema_str)

string_serializer = StringSerializer('utf_8')

producer = Producer(conf)



def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    # print('Keyterm record {} successfully produced to {} [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))


def send_msg(topic, key, msg):
    producer.produce(
        topic,
        key=string_serializer(key),
        value=avro_serializer(msg, SerializationContext(topic, MessageField.VALUE)),
        on_delivery=delivery_report
    )




def send(
    topic:str = None,
    platform: str = None,
    keyterms: str = None,
    user_id: int = None,
    organization_id: int = None,
    **kwargs):
    if not user_id or not organization_id\
        or not keyterms or not platform:

        raise ValueError("All parameters must be passed platform, "
                         "keyterms, uesr_id, organization_id!")

    MSG['user_id'] = user_id
    MSG["organization_id"] = organization_id
    MSG['platform'] = platform
    MSG["key_term"] = keyterms.lower()
    # MSG["kwargs"] = {**kwargs}
    # msg_str = json.dumps(MSG).encode('utf-8')

    send_msg(
        topic=topic,
        key=str(user_id)+str(organization_id)+keyterms+platform,
        msg=MSG
    )


if __name__ == "__main__":
    args = parser.parse_args()
    users = [1,2,3,4,5,6,7]
    orgs = [12,13,14,15,16,17]
    platforms = ["A", "B", "C", "D", "E", "F"]
    keyterms = ["dubai Economy", "Industry", "Fifa world cop", 'Formula1 races']

    for i in range(1000000):
        send(
            topic=args.topic,
            user_id=random.choice(users),
            organization_id=random.choice(orgs),
            platform=random.choices(platforms)[0],
            keyterms=random.choice(keyterms)
            )
        if i%1000==0:
            producer.flush()
    producer.flush()
