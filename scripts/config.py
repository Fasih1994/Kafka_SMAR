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

# Twitter
POSTS_TOPIC = "posts"
POST_TASKS_TOPIC = "post_tasks"
POST_TASKS_FINISHED_TOPIC = "post_task_finished"
COMMENTS_TOPIC = "comments"
COMMENT_TASKS_TOPIC = "comment_tasks"
COMMENT_TASKS_FINISHED_TOPIC = "comment_tasks_finished"

# Facebook
FACEBOOK_POSTS_TOPIC = "facebook_posts"
FACEBOOK_POST_TASKS_TOPIC = "facebook_post_tasks"
FACEBOOK_POST_TASKS_FINISHED_TOPIC = "facebook_post_task_finished"
FACEBOOK_COMMENTS_TOPIC = "facebook_comments"
FACEBOOK_COMMENT_TASKS_TOPIC = "facebook_comment_tasks"
FACEBOOK_COMMENT_TASKS_FINISHED_TOPIC = "facebook_comment_tasks_finished"

# Instagram
INSTAGRAM_POSTS_TOPIC = "instagram_posts"
INSTAGRAM_POST_TASKS_TOPIC = "instagram_post_tasks"
INSTAGRAM_POST_TASKS_FINISHED_TOPIC = "instagram_post_task_finished"
INSTAGRAM_COMMENTS_TOPIC = "instagram_comments"
INSTAGRAM_COMMENT_TASKS_TOPIC = "instagram_comment_tasks"
INSTAGRAM_COMMENT_TASKS_FINISHED_TOPIC = "instagram_comment_tasks_finished"



# SCHEMAS
with open(os.path.join(avro_schema_path, 'keyterm.avsc')) as f:
    KEY_TERM_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'tasks.avsc')) as f:
    TASKS_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'post.avsc')) as f:
    POST_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'comment.avsc')) as f:
    COMMENT_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'facebook_post.avsc')) as f:
    FACEBOOK_POST_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'facebook_comment.avsc')) as f:
    FACEBOOK_COMMENT_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'instagram_post.avsc')) as f:
    INSTAGRAM_POST_SCHEMA = f.read()

with open(os.path.join(avro_schema_path, 'instagram_comment.avsc')) as f:
    INSTAGRAM_COMMENT_SCHEMA = f.read()
