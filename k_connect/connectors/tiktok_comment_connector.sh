# Get the first IP address from the output of hostname -I
MY_IP=$(hostname -I | awk '{print $1}')

# Use the extracted IP address in your connector configuration
CONNECTOR_CONF='{
    "name": "tiktok-comment-sink",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics": "tiktok_comments",
        "connection.url": "jdbc:sqlserver://'${MY_IP}';databaseName=TEST_DB",
        "connection.user": "sa",
        "connection.password": "Fasih!23",
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
