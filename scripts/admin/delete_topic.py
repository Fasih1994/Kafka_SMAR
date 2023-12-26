import argparse
from confluent_kafka.admin import AdminClient, NewTopic

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--topic', type=str,
                    help='Comma-separated list of topics to delete.')

admin_conf = {
    "bootstrap.servers": "localhost:9093,localhost:9094,localhost:9095"
}

if __name__ == "__main__":
    args = parser.parse_args()
    admin = AdminClient(admin_conf)

    # Convert the comma-separated list of topics to a list
    topics_to_delete = args.topic.split(',')

    # Delete topics
    result = admin.delete_topics(topics_to_delete, operation_timeout=30)

    for topic, f in result.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except Exception as e:
            print("Failed to delete topic {}: {}".format(topic, e))
