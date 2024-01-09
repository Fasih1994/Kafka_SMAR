#/bin/zsh
# echo "Creating network k_cluster_net"
docker network create -d bridge cluster_default
echo "STARTING ZOOKEEPER"
docker compose -f $(pwd)/cluster/docker_compose.yml up -d zookeeper

sleep 20
echo "STARTING KAFKA_CLUSTER"
docker compose -f $(pwd)/cluster/docker_compose.yml up -d kafka1 kafka2 kafka3

sleep 5
echo "STARTING KAFKA_SCHEMA_REGISTRY"
docker compose -f $(pwd)/cluster/docker_compose.yml up -d schema-registry

sleep 5
echo "STARTING KAFKA_CONNECT"
docker compose -f $(pwd)/k_connect/docker_compose.yml up -d kafka-connect
# echo "Starting Kafka brokers 1, 2, 3"
# docker compose -f $(pwd)/kafka_1/docker_compose.yml up -d
# docker compose -f $(pwd)/kafka_2/docker_compose.yml up -d
# docker compose -f $(pwd)/kafka_3/docker_compose.yml up -d
# sleep 3
# echo "Starting Schema Registry"
# docker compose -f $(pwd)/schema_registry/docker_compose.yml up -d
# # sleep 3
# echo "Starting Kafka connect"
# docker compose -f $(pwd)/k_connect/docker_compose.yml up -d
# sleep 3
echo "Done!"
