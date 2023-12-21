import os
import socket
from dotenv import load_dotenv
load_dotenv()


producer_conf = {
    'bootstrap.servers': 'localhost:9093,localhost:9094,localhost:9095',
    'client.id': socket.gethostname(),
    'enable.idempotence': True
    }


twitter_post_base_param = {
    'access_token': os.environ['DATA365_KEY'],
    'max_page_size': 100,
    'order_by': "date_asc"
}


consumer_conf = {
    'bootstrap.servers': 'localhost:9093,localhost:9094,localhost:9095',
    'auto.offset.reset': "earliest"
    }


schema_registry_conf = {'url': 'http://localhost:8081'}


avro_schema_path = "/home/fasih/k_cluster_smar/schema/avro"


# TOPICS
KEY_TERM_TOPIC = "keyterm"
POST_TASKS_TOPIC = "post_tasks"
POST_TASKS_FINISHED_TOPIC = "post_task_finished"
POSTS_TOPIC = "posts"
COMMENT_TASKS_TOPIC = "comment_tasks"
COMMENT_TASKS_FINISHED_TOPIC = "comment_tasks_finished"
COMMENTS_TOPIC = "comments"


# SCHEMAS
with open(os.path.join(avro_schema_path, 'keyterm.avsc')) as f:
    KEY_TERM_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'tasks.avsc')) as f:
    TASKS_SCHEMA = f.read()
