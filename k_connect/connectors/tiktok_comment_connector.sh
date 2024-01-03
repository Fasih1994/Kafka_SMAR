# Get the first IP address from the output of hostname -I
MY_IP=$(hostname -I | awk '{print $1}')

# Use the extracted IP address in your connector configuration
CONNECTOR_CONF='{
    "name": "tiktok-comment-sink",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics": "tiktok_comments",
        "connection.url": "'$CONNECTION_URL'",
        "connection.user": "'$DB_USER'",
        "connection.password": "'$DB_PASSWORD'",
        "auto.create": "true",
        "insert.mode": "upsert",
        "value.converter": "io.confluent.connect.avro.AvroConverter",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter.schema.registry.url": "http://schema-registry:8081",
        "auto.offset.reset": "earliest",
        "pk.mode": "record_value",
        "pk.fields": "id,user_id,organization_id,project_id",
        "auto.evolve": true
    }
}'

# Send the connector configuration using curl
curl -s -X POST -H 'Content-Type: application/json' --data "${CONNECTOR_CONF}" http://localhost:8083/connectors | jq
