from time import sleep
from urllib.parse import unquote

from confluent_kafka import Consumer, Producer, TopicPartition
from confluent_kafka.serialization import SerializationContext, MessageField

from utils import get_logger, get_data, transform_data
from scripts.config import (
    consumer_conf,
    producer_conf,
    LINKEDIN_POST_TASKS_FINISHED_TOPIC,
    LINKEDIN_POSTS_TOPIC
)

from scripts.utils import (
    task_deserializer,
    string_serializer,
    linkedin_post_serializer
)


logger = get_logger("SMAR")


def get_post_url(url: str=None)-> str:
    url = url.replace(
        "/update",
        "/posts"
    )
    return url


def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Post record {}: {}".format(msg.key(), err))
        return
    # logger.info('Post record {} successfully produced to {} parttition [{}] at offset {}'.format(
    #     msg.key(), msg.topic(), msg.partition(), msg.offset()))


def produce_post(msg=None, posts: list=None):
    producer = Producer(producer_conf)

    for post in posts:
        key = str(post['id'])+str(post['organization_id'])+str(post['user_id'])+str(post['project_id'])
        producer.produce(
            LINKEDIN_POSTS_TOPIC,
            key=string_serializer(key),
            value=linkedin_post_serializer(post, SerializationContext(LINKEDIN_POSTS_TOPIC, MessageField.VALUE)),
            on_delivery=delivery_report
        )
    producer.flush()
    logger.info(f"produced {len(posts)} posts.")
    return True


def get_post_data(msg=None, task_data: dict=None):
    # check task status
    post_url = get_post_url(task_data['url'])

    # get key word from url
    keyword = unquote(post_url.split('/')[6])
    data_available = True
    cursor = None
    tries = 0

    while data_available:
        if cursor:
            data = get_data(url=post_url, page=cursor )
        else:
            data = get_data(url=post_url )

        if data:
            posts = data['items']
            posts = transform_data(
                items=posts,
                keyword=keyword,
                task_data=task_data)
            produced = produce_post(msg=msg, posts=posts)

            if not produced:
                return False
            if data['page_info']['has_next_page']:
                cursor = data['page_info']['cursor']
            else:
                data_available = False
        else:
            tries+=1
            if tries==3:
                logger.error(f"Empty data returned by {post_url} in 3 tries.")
                data_available = False
                produced = True
            else:
                sleep(0.3)
                continue
    return True


def main():
    consumer_conf['group.id'] = 'linkedin_get_post_data'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([LINKEDIN_POST_TASKS_FINISHED_TOPIC])
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
                try:
                    finished = get_post_data(msg=msg, task_data=task_data)
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
