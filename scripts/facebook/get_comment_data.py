import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


from urllib.parse import urlparse, parse_qs
from time import sleep

from confluent_kafka import Consumer, Producer, TopicPartition
from confluent_kafka.serialization import SerializationContext, MessageField

from utils import get_logger, get_data, transform_data
from scripts.config import (
    twitter_post_base_param,
    consumer_conf,
    producer_conf,
    FACEBOOK_COMMENT_TASKS_FINISHED_TOPIC,
    FACEBOOK_COMMENTS_TOPIC
)

from scripts.utils import (
    task_deserializer,
    facebook_comment_serializer
)


logger = get_logger("SMAR")


def get_comment_url(url: str=None)-> str:
    url = url.split("?")[0]
    url = url.replace(
        "/update",
        "/comments"
    )
    return url


def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Post record {}: {}".format(msg.key(), err))
        return
    # logger.info('Post record {} successfully produced to {} parttition [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))


def produce_comment(msg=None, comments: list=None, url: str=None):
    producer = Producer(producer_conf)
    producer.flush()

    for comment in comments:
        producer.produce(
            FACEBOOK_COMMENTS_TOPIC,
            key=msg.key(),
            value=facebook_comment_serializer(comment, SerializationContext(FACEBOOK_COMMENTS_TOPIC, MessageField.VALUE)),
            on_delivery=delivery_report
        )
    producer.flush()
    logger.info(f"produced {len(comments)} comments for {url}.")
    return True


def get_comments_data(msg=None, task_data: dict=None):
    # check task status
    comments_url = get_comment_url(task_data['url'])

    # get key word from url
    data_available = True
    cursor = None
    tries = 0


    while data_available:
        params = {
            "access_token": twitter_post_base_param['access_token'],
            "order_by": "date_desc",
            "max_page_size": 100
        }

        if cursor:
            params['cursor']=cursor
            data = get_data(url=comments_url, params=params)
        else:
            data = get_data(url=comments_url, params=params )

        if data:
            comments = data['items']
            comments = transform_data(
                items=comments,
                task_data=task_data)
            produced = produce_comment(msg=msg,
                                       comments=comments,
                                       url=comments_url)

            if not produced:
                return False
            if data['page_info']['has_next_page']:
                cursor = data['page_info']['cursor']
            else:
                data_available = False
        else:
            tries+=1
            if tries==3:
                logger.error(f"Empty data returned by {comments_url} in 3 tries.")
                data_available = False
            else:
                sleep(0.3)
                continue
    return True


def main():
    consumer_conf['group.id'] = 'facebook_get_comments_data'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([FACEBOOK_COMMENT_TASKS_FINISHED_TOPIC])
    WAIT_COUNT = 0
    logger.info(f'Starting consumer {consumer_conf["group.id"]}')

    while True:
        try:
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
                if task_data['platform'] == 'facebook':
                    try:
                        finished = get_comments_data(msg=msg, task_data=task_data)
                        if finished:
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
