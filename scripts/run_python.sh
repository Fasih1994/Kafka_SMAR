#!/bin/bash

# Set the Kafka bootstrap server and consumer group
BOOTSTRAP_SERVER="localhost:9093,localhost:9094,localhost:9095"
CONSUMER_GROUP="pipeline"
TOPIC="pipeline1"

ROOT_DIR=/home/fasih/k_cluster_smar

# Run the kafka-consumer-groups command within the Docker container and filter the relevant information
current_time=$(date +"%Y-%m-%d %H:%M:%S")
UNIQUE_CONSUMER_COUNT=$($ROOT_DIR/venv/bin/python $ROOT_DIR/scripts/member_count.py -g $CONSUMER_GROUP)

# Print the count of unique consumer IDs
echo "$current_time - Number of unique consumer IDs in group '$CONSUMER_GROUP': $UNIQUE_CONSUMER_COUNT"

# Check if the count is less than 3
if [ $UNIQUE_CONSUMER_COUNT -lt 1 ]; then
    echo "$current_time - Count is less than 1. Running Python script..."
    # Execute your Python script here
    $ROOT_DIR/venv/bin/python $ROOT_DIR/scripts/consume_keyterms.py \
    -t $TOPIC \
    -g $CONSUMER_GROUP >> "$ROOT_DIR/consumer_logs/$current_time-$CONSUMER_GROUP.log"
else
    echo "Consumer already Up."
fi