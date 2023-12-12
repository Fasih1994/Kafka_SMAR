#/bin/bash
# docker compose -f $(pwd)/k_connect/docker_compose.yml down
# docker compose -f $(pwd)/schema_registry/docker_compose.yml down
# docker compose -f $(pwd)/kafka_3/docker_compose.yml down
# docker compose -f $(pwd)/kafka_2/docker_compose.yml down
# docker compose -f $(pwd)/kafka_1/docker_compose.yml down
docker compose -f $(pwd)/cluster/docker_compose.yml down
# echo "Remoivng network k_cluster_net"
# docker network rm k_cluster_net
