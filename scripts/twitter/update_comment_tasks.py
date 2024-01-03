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
    twitter_post_base_param,
    POSTS_TOPIC,
    COMMENT_TASKS_TOPIC
)

from scripts.utils import (
    post_deserializer,
    task_serializer,
    string_serializer
)
logger = get_logger("SMAR")

def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Comment record {}: {}".format(msg.key(), err))
        return
    # logger.info('Comment record {} successfully produced to {} in partition [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))


def update_comment_task(msg=None, post_data: dict=None):
    update_url = "https://api.data365.co/v1.1/twitter/profile/{profile_id}/feed/posts/{post_id}/update"
    params = {
        "access_token": twitter_post_base_param['access_token'],
        "load_replies": "true",
        "max_replies": 100
    }
    url_to_use = update_url.format(
        profile_id=post_data["author_username"],
        post_id=post_data["id"]
    )

    r = requests.post(
            url_to_use,
            params=params
        )
    if r.status_code == 202:
        producer = Producer(producer_conf)
        data = dict(
            user_id = post_data['user_id'],
            organization_id = post_data['organization_id'],
            project_id = post_data['project_id'],
            platform = "twitter",
            url = r.url
        )
        logger.info(
            f"Updated Taks for {data}"
        )
        producer.produce(
            COMMENT_TASKS_TOPIC,
            key=string_serializer(r.url),
            value=task_serializer(data, SerializationContext(COMMENT_TASKS_TOPIC, MessageField.VALUE)),
            on_delivery=delivery_report
        )
        producer.flush()
        return True
    logger.error(f"got {r.status_code} for {r.url} with {r.json()}")
    return False



def main():
    consumer_conf['group.id'] = 'twitter_update_comment_tasks'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([POSTS_TOPIC])
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
                post_data = post_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                WAIT_COUNT=0
                # Check if tweet has comments
                if post_data['reply_count']==0:
                    continue
                try:
                    updated = update_comment_task(msg=msg, post_data=post_data)
                    if updated:
                        consumer.commit()
                except Exception as e:
                    tp = TopicPartition(msg.topic(), msg.partition(), msg.offset())
                    consumer.seek(tp)
                    logger.error(e)
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
