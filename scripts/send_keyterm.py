"""
Send Keyterm object to Kafka Topic

"""
import random

from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField

from config import (
    producer_conf,
    KEY_TERM_TOPIC
)
from utils import (
    string_serializer,
    keyterm_serializer
)

MSG = {
    "user_id": None,
    "organization_id": None,
    "key_term": None,
    "platform": None,
    "from_date": None,
    "to_date": None,
}


producer = Producer(producer_conf)



def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for Keyterm record {}: {}".format(msg.key(), err))
        return
    print('Keyterm record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def send_msg(topic, key, msg):
    producer.produce(
        topic,
        key=string_serializer(key),
        value=keyterm_serializer(msg, SerializationContext(topic, MessageField.VALUE)),
        on_delivery=delivery_report
    )


def send_keyterm(
    platform: str = None,
    keyterms: str = None,
    from_date: str = None,
    to_date: str = None,
    user_id: int = None,
    organization_id: int = None,
    project_id: int = None,
    **kwargs):
    if not user_id or not organization_id\
        or not keyterms or not platform \
        or not project_id:

        raise ValueError("All parameters must be passed platform, "
                         "keyterms, uesr_id, organization_id!")

    if (to_date and not from_date) or (not to_date and from_date):
        raise ValueError('Both date params must be provided if '
                         'any of [to_date or from_date] is passed')

    MSG['user_id'] = user_id
    MSG["organization_id"] = organization_id
    MSG["project_id"] = project_id
    MSG['platform'] = platform
    MSG["key_term"] = keyterms.lower()
    MSG["from_date"] = from_date
    MSG["to_date"] = to_date

    key = str(user_id)+str(organization_id)+str(project_id)+keyterms+platform
    key = key + to_date if to_date else ""
    key = key + from_date if from_date else ""

    send_msg(
        topic=KEY_TERM_TOPIC,
        key=key,
        msg=MSG
    )


if __name__ == "__main__":
    users = [1,2,3,4,5,6,7]
    orgs = [12,13,14,15,16,17]
    projects = [122,133,144,155,166,177]
    platforms = ["A", "B", "C", "D", "E", "F"]
    keyterms = ["dubai Economy", "Industry", "Fifa world cup", 'Formula1 races']
    from_dates = ['2021-01-1','2020-11-12','2021-03-30','2020-09-10','2021-02-30', None]
    from_dates = ['2022-01-1','2023-11-12','2022-03-30','2023-09-10','2023-02-30', None]

    for i in range(1):
        try:

            send_keyterm(
                user_id=random.choice(users),
                project_id=random.choice(projects),
                organization_id=random.choice(orgs),
                platform=random.choices(platforms)[0],
                keyterms=random.choice(keyterms),
                from_date='2021-01-1',
                to_date='2022-12-31'
                )
            if i%1000==0:
                producer.flush()

        except ValueError as e:
            print(str(e))
            continue
    producer.flush()
