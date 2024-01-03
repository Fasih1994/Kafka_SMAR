import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import requests

from confluent_kafka import Consumer, Producer, TopicPartition
from confluent_kafka.serialization import SerializationContext, MessageField

from utils import get_logger
from scripts.config import (
    consumer_conf,
    producer_conf,
    INSTAGRAM_POST_TASKS_TOPIC,
    INSTAGRAM_POST_TASKS_FINISHED_TOPIC
)
from scripts.utils import (
    task_serializer,
    task_deserializer
)

pendind_tasks = {}

logger = get_logger("SMAR")

def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Task record {}: {}".format(msg.key(), err))
        return
    # logger.info('Task record {} successfully produced to {} parttition [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))


def check_post_task(msg=None, task_data: dict=None):
    # check if task is pending task
    r = requests.get(task_data['url'])

    if r.status_code == 200:
        producer = Producer(producer_conf)
        response = r.json()
        if response['data']['status']=='finished':
           # if task is finished send to finished Topic
            logger.info(
                f"Finished Task for {task_data}"
            )
            producer.produce(
                INSTAGRAM_POST_TASKS_FINISHED_TOPIC,
                key=msg.key(),
                value=task_serializer(
                    task_data,
                    SerializationContext(INSTAGRAM_POST_TASKS_FINISHED_TOPIC, MessageField.VALUE)),
                on_delivery=delivery_report
            )
            producer.flush()
            return True

        elif response['data']['status'] in ("pending", "created"):
            # if task is pending add to cache
            producer.produce(
                INSTAGRAM_POST_TASKS_TOPIC,
                key=msg.key(),
                value=task_serializer(task_data, SerializationContext(INSTAGRAM_POST_TASKS_TOPIC, MessageField.VALUE)),
                on_delivery=delivery_report
            )
            producer.flush()

        elif response['data']['status'] in ("fail", "canceled"):
            # if task fails log the error
            logger.error(
                f"Task failed for {task_data}"
            )
            return True

    return False


def main():
    consumer_conf['group.id'] = 'instagram_check_post_tasks'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([INSTAGRAM_POST_TASKS_TOPIC])
    WAIT_COUNT = 0
    logger.info(f'Starting consumer {consumer_conf["group.id"]}')

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(20)
            if msg is None:
                WAIT_COUNT += 1
                if WAIT_COUNT == 7:
                    logger.info(f'Closing consumer {consumer_conf["group.id"]}')
                    break
                continue

            if msg is not None:
                task_data = task_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                WAIT_COUNT=0
                if task_data['platform'] == 'instagram':
                    try:
                        finished = check_post_task(msg=msg, task_data=task_data)
                        if finished:
                            consumer.commit()
                    except Exception as e:
                        tp = TopicPartition(msg.topic(), msg.partition(), msg.offset())
                        consumer.seek(tp)
                        logger.error(e)
                else:
                    consumer.commit()


        except KeyboardInterrupt:
            break

    consumer.close()
    logger.info("All task completed for instagram posts.")


if __name__ == '__main__':
    main()
