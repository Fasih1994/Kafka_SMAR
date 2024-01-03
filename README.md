# kafka-cluster

This is a Kafka Cluster setup with confluent stack, it includes

* Zookeeper
* Kafka
* Kafka Connect
* Schema Registry
* Python

# Kafka_SMAR

# Commands
- reset group offset to 0
`kafka-consumer-groups --bootstrap-server localhost:9092 --group twitter_get_comments_data --reset-offsets --to-earliest --execute --topic comments`

- Create all topics
`python scripts/admin/create_topic.py -t posts,post_tasks,post_task_finished,comments,comment_tasks,comment_tasks_finished`

- delete all topics
`python scripts/admin/delete_topic.py -t posts,post_tasks,post_task_finished,comments,comment_tasks,comment_tasks_finished`

- CREATE TWITTER POST CONNECTOR
`curl -s -X POST -H 'Content-Type: application/json' --data @k_connect/connectors/posts_connector.json http://localhost:8083/connectors | jq`

- DELETE TWITTER POSTS CONNECTOR
`curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/posts-sink/ | jq`


- CREATE TWITTER COMMENTS CONNECTOR
`curl -s -X POST -H 'Content-Type: application/json' --data @k_connect/connectors/twitter_comments_connector.json http://localhost:8083/connectors | jq`

- DELETE TWITTER COMMENTS CONNECTOR
`curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/twitter-comment-sink/ | jq`

- Start all consumers for twitter
`./scripts/shell/twitter/run_all.sh`

- Check running tasks
`ps aux | grep k_cluster_smar`

- create & delete topic
`export platform='linkedin'`
`python scripts/admin/delete_topic.py -t ${platform}_posts,${platform}_post_tasks,${platform}_post_task_finished,${platform}_comments,${platform}_comment_tasks,${platform}_comment_tasks_finished`