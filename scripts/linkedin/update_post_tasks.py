import requests

from confluent_kafka import Consumer, Producer, TopicPartition
from confluent_kafka.serialization import SerializationContext, MessageField

from utils import get_logger
from scripts.config import (
    consumer_conf,
    producer_conf,
    twitter_post_base_param,
    KEY_TERM_TOPIC,
    LINKEDIN_POST_TASKS_TOPIC
)

from scripts.utils import (
    keyterm_deserializer,
    task_serializer
)
logger = get_logger("SMAR")

def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for Keyterm record {}: {}".format(msg.key(), err))
        return
    logger.info('Keyterm record {} successfully produced to {} in partition [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def update_post_task(msg=None, term_data: dict=None):

    update_url = "https://api.data365.co/v1.1/instagram/tag/{tag_id}/update"
    update_url = update_url.format(
        tag_id="".join(term_data['key_term'].split())
    )

    params = {
        "access_token": twitter_post_base_param['access_token']
    }

    if term_data['from_date'] and term_data['from_date']!='':
        params['from_date'] = term_data['from_date']
        params['to_date'] = term_data['to_date']

    r = requests.post(
            update_url,
            params=params
        )
    if r.status_code == 202:
        logger.info(
            f"Updated Taks for {term_data}"
        )
        producer = Producer(producer_conf)
        data = dict(
            user_id = term_data['user_id'],
            organization_id = term_data['organization_id'],
            project_id = term_data['project_id'],
            platform = term_data['platform'],
            url = r.url
        )
        producer.produce(
            LINKEDIN_POST_TASKS_TOPIC,
            key=msg.key(),
            value=task_serializer(data, SerializationContext(LINKEDIN_POST_TASKS_TOPIC, MessageField.VALUE)),
            on_delivery=delivery_report
        )
        producer.flush()
        return True
    logger.error(f"got {r.status_code} for {r.url} with {r.json()}")
    return False



def main():
    consumer_conf['group.id'] = 'linkedin_update_post_tasks'
    consumer = Consumer(consumer_conf)
    consumer.subscribe([KEY_TERM_TOPIC])
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
                term_data = keyterm_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))
                WAIT_COUNT=0
                if term_data['platform'] == 'linkedin':
                    try:
                        updated = update_post_task(msg=msg, term_data=term_data)
                        if updated:
                            consumer.commit()
                        else:
                            raise ValueError(f"Update failed for key: {msg.key()}")
                    except Exception as e:
                        tp = TopicPartition(msg.topic(), msg.partition(), msg.offset())
                        consumer.seek(tp)
                        logger.error(e)
                else:

                    consumer.commit()
        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == '__main__':
    main()
