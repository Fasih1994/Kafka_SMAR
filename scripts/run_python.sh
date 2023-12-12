#!/bin/bash

# Set the Kafka bootstrap server and consumer group
BOOTSTRAP_SERVER="localhost:9093,localhost:9094,localhost:9095"
CONSUMER_GROUP="pipeline0"
TOPIC="test"
ITERATIONS=6


# Run the kafka-consumer-groups command within the Docker container and filter the relevant information
UNIQUE_CONSUMER_COUNT=$(docker exec -it kafka1 sh -c "kafka-consumer-groups --bootstrap-server $BOOTSTRAP_SERVER --group $CONSUMER_GROUP --describe" | awk 'NR>2' | awk '{print $7}' | sort -u | wc -l)

# Print the count of unique consumer IDs
echo "Number of unique consumer IDs in group '$CONSUMER_GROUP': $UNIQUE_CONSUMER_COUNT"

# Check if the count is less than 3
if [ $UNIQUE_CONSUMER_COUNT -lt 4 ]; then
    echo "Count is less than 4. Running Python script..."
    # Execute your Python script here
    python start_consumer.py --consumer-number $UNIQUE_CONSUMER_COUNT \
    --topic $TOPIC \
    --broker $BOOTSTRAP_SERVER \
    --group $CONSUMER_GROUP >> $CONSUMER_GROUP.log
else
    echo "Count is 4 or more. No need to run the Python script."
fi