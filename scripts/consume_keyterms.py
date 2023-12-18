import argparse
import os

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer


class User(object):
    """
    User record

    Args:
        name (str): User's name

        favorite_number (int): User's favorite number

        favorite_color (str): User's favorite color
    """

    def __init__(self, name=None, favorite_number=None, favorite_color=None):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color


def dict_to_user(obj, ctx):
    """
    Converts object literal(dict) to a User instance.

    Args:
        obj (dict): Object literal(dict)

        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    """

    if obj is None:
        return None

    return User(name=obj['name'],
                favorite_number=obj['favorite_number'],
                favorite_color=obj['favorite_color'])


def main(args):
    topic = args.topic

    schema = 'keyterm.avsc'
    path = os.path.realpath(os.path.dirname(__file__))
    with open(f"{path}/schema/avro/{schema}") as f:
        schema_str = f.read()

    sr_conf = {'url': 'http://localhost:8081'}
    schema_registry_client = SchemaRegistryClient(sr_conf)

    avro_deserializer = AvroDeserializer(schema_registry_client,
                                         schema_str)

    consumer_conf = {'bootstrap.servers': 'localhost:9093,localhost:9094,localhost:9095',
                     'group.id': args.group,
                     'auto.offset.reset': "earliest"}

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    WAIT_COUNT = 0

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                print('waiting...')
                WAIT_COUNT += 1
                if WAIT_COUNT > 7:
                    break
                continue

            msg = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
            if msg is not None:
                WAIT_COUNT=0
                print(
                    msg['user_id'],
                    msg['organization_id'],
                    msg['key_term'],
                    msg['platform'],
                    end='\n'
                )
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AvroDeserializer example")
    parser.add_argument('-t', dest="topic", default="example_serde_avro",
                        help="Topic name")
    parser.add_argument('-g', dest="group", default="example_serde_avro",
                        help="Consumer group")

    main(parser.parse_args())