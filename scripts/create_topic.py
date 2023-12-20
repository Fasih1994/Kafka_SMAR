import argparse
from confluent_kafka.admin import AdminClient, NewTopic

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--topic', type=str,
                    help='Groupd whose members needs to be count.')

admin_conf = {
    "bootstrap.servers": "localhost:9093,localhost:9094,localhost:9095"
}

if __name__=="__main__":
    args = parser.parse_args()
    admin = AdminClient(admin_conf)

    topics = [NewTopic(topic,
                     num_partitions = 3,
                     replication_factor = 2)
              for topic in args.topic.split(',')]

    result = admin.create_topics(topics)
    for topic, f in result.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
