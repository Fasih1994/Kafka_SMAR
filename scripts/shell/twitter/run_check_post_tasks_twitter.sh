#!/bin/bash

# Set the Kafka bootstrap server and consumer group
BOOTSTRAP_SERVER="localhost:9093,localhost:9094,localhost:9095"
CONSUMER_GROUP="twitter_check_post_tasks"

if [ "$ENVIRONMENT" == "dev" ]; then
    ROOT_DIR="/home/fasih/k_cluster_smar"
elif [ "$ENVIRONMENT" == "prod" ]; then
    ROOT_DIR="/home/django/Kafka_SMAR"
fi

# Run the kafka-consumer-groups command within the Docker container and filter the relevant information
current_time=$(date +"%Y-%m-%d %H:%M:%S")
UNIQUE_CONSUMER_COUNT=$($ROOT_DIR/venv/bin/python $ROOT_DIR/scripts/admin/member_count.py -g $CONSUMER_GROUP)

# Print the count of unique consumer IDs
echo "$current_time - Number of unique consumer IDs in group '$CONSUMER_GROUP': $UNIQUE_CONSUMER_COUNT"

# Check if the count is less than 3
if [ $UNIQUE_CONSUMER_COUNT -lt 1 ]; then
    echo "$current_time - Count is less than 1. Running Python script..."
    # Execute your Python script here
    $ROOT_DIR/venv/bin/python -u $ROOT_DIR/scripts/twitter/check_post_tasks.py
else
    echo "Consumer already Up."
fi