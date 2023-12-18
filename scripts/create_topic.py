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
    topic = NewTopic(args.topic,
                     num_partitions = 3,
                     replication_factor = 2)

    result = admin.create_topics([topic])
    print(f"Topics {args.topic} created succesfully!")