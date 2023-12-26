from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer

from scripts.config import (
    schema_registry_conf,
    KEY_TERM_SCHEMA,
    TASKS_SCHEMA,
    POST_SCHEMA
)


schema_registry_client = SchemaRegistryClient(schema_registry_conf)


# SERIALIZER
string_serializer = StringSerializer('utf_8')
keyterm_serializer = AvroSerializer(schema_registry_client,
                                    KEY_TERM_SCHEMA)
task_serializer = AvroSerializer(schema_registry_client,
                                    TASKS_SCHEMA)
post_serializer = AvroSerializer(schema_registry_client,
                                    POST_SCHEMA)

#DESERIALIZER
keyterm_deserializer = AvroDeserializer(schema_registry_client,
                                         KEY_TERM_SCHEMA)
task_deserializer = AvroDeserializer(schema_registry_client,
                                    TASKS_SCHEMA)
post_deserializer = AvroDeserializer(schema_registry_client,
                                    POST_SCHEMA)