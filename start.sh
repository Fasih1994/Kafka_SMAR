#/bin/zsh
echo "Creating network k_cluster_net"
docker network create -d bridge k_cluster_net
echo "Starting zookeeper"
docker compose -f $(pwd)/zookeeper/docker_compose.yml up -d
sleep 3
echo "Starting Kafka brokers 1, 2, 3"
docker compose -f $(pwd)/kafka_1/docker_compose.yml up -d
docker compose -f $(pwd)/kafka_2/docker_compose.yml up -d
docker compose -f $(pwd)/kafka_3/docker_compose.yml up -d
sleep 3
echo "Starting Schema Registry"
docker compose -f $(pwd)/schema_registry/docker_compose.yml up -d
sleep 3
echo "Starting Kafka connect"
docker compose -f $(pwd)/k_connect/docker_compose.yml up -d
sleep 3
echo "Done!"
