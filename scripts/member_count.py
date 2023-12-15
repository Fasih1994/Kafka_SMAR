import argparse
from confluent_kafka.admin import AdminClient

parser = argparse.ArgumentParser()

parser.add_argument('-g', '--group', type=str,
                    help='Groupd whose members needs to be count.')

admin_conf = {
    "bootstrap.servers": "localhost:9093,localhost:9094,localhost:9095"
}

if __name__=="__main__":
    args = parser.parse_args()
    admin = AdminClient(admin_conf)
    group_map = admin.describe_consumer_groups([args.group])
    group_details = group_map[args.group].result()
    print(len(group_details.members))