from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField

from scripts.config import (
    consumer_conf,
    KEY_TERM_TOPIC,
    POST_TASKS_TOPIC
)

from scripts.utils import (
    keyterm_deserializer,
    task_serializer
)


def main():
    consumer_conf['group.id'] = 'twitter_update_post_tasks'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([KEY_TERM_TOPIC])
    WAIT_COUNT = 0

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(10)
            if msg is None:
                WAIT_COUNT += 1
                if WAIT_COUNT == 7:
                    break
                continue

            if msg is not None:
                msg = keyterm_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                WAIT_COUNT=0
                print(msg)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
