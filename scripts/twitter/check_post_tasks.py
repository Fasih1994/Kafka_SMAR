import requests

from confluent_kafka import Consumer, Producer, TopicPartition
from confluent_kafka.serialization import SerializationContext, MessageField

from utils import get_logger
from scripts.config import (
    consumer_conf,
    producer_conf,
    POST_TASKS_TOPIC,
    POST_TASKS_FINISHED_TOPIC
)
from scripts.utils import (
    task_serializer,
    task_deserializer
)
from scripts.models import PendingTask

pendind_tasks = {}

logger = get_logger("SMAR")

def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Task record {}: {}".format(msg.key(), err))
        return
    logger.info('Task record {} successfully produced to {} parttition [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def check_post_task(msg=None, task_data: dict=None, pending: bool=False):
    # check if task is pending task
    if not pending:
        r = requests.get(task_data['url'])
    else:
        task = pendind_tasks.get(msg.key())
        task.tried()

        print(task.msg.key(), task.tries)
        if task.tries%3 == 0:
            r = requests.get(task_data['url'])
        else:
            return False

    if r.status_code == 200:
        producer = Producer(producer_conf)
        response = r.json()
        if response['data']['status']=='finished':
           # if task is finished send to finished Topic
            logger.info(
                f"Finished Task for {task_data}"
            )
            producer.produce(
                POST_TASKS_FINISHED_TOPIC,
                key=msg.key(),
                value=task_serializer(task_data, SerializationContext(POST_TASKS_TOPIC, MessageField.VALUE)),
                on_delivery=delivery_report
            )
            producer.flush()
            return True

        elif response['data']['status'] in ("pending", "created"):
            # if task is pending add to cache
            if not pending:
                task = PendingTask(msg=msg,task=task_data,tries=15)
                pendind_tasks[msg.key()] = task
            else:
                return False

        elif response['data']['status'] in ("fail", "canceled"):
            # if task fails log the error
            logger.error(
                f"Task failed for {task_data}"
            )
            return True

    return False



def main():
    consumer_conf['group.id'] = 'twitter_check_post_tasks'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([POST_TASKS_TOPIC])
    WAIT_COUNT = 0

    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(20)
            if msg is None:
                WAIT_COUNT += 1
                if WAIT_COUNT>3:
                    logger.info("Checking Pending Tasks")
                    while pendind_tasks:
                        for k, v in list(pendind_tasks.items()):
                            finished = check_post_task(
                                msg=v.msg, task_data=v.task,
                                pending=True)
                            if finished:
                                pendind_tasks.pop(k)
                if WAIT_COUNT == 7:
                    logger.info(f'Closing consumer {consumer_conf["group.id"]}')
                    break
                continue

            if msg is not None:
                task_data = task_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                WAIT_COUNT=0
                if task_data['platform'] == 'twitter':
                    try:
                        finished = check_post_task(msg=msg, task_data=task_data)
                        if finished:
                            consumer.commit()
                    except Exception as e:
                        tp = TopicPartition(msg.topic(), msg.partition(), msg.offset())
                        consumer.seek(tp)
                        logger.error(e)
        except KeyboardInterrupt:
            break

    consumer.close()
    logger.info("All task completed.")


if __name__ == '__main__':
    main()
