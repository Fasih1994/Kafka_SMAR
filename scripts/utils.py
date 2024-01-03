from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer

from scripts.config import (
    schema_registry_conf,
    KEY_TERM_SCHEMA, TASKS_SCHEMA,
    POST_SCHEMA, COMMENT_SCHEMA,
    FACEBOOK_POST_SCHEMA, FACEBOOK_COMMENT_SCHEMA,
    INSTAGRAM_POST_SCHEMA, INSTAGRAM_COMMENT_SCHEMA,
    LINKEDIN_POST_SCHEMA, LINKEDIN_COMMENT_SCHEMA,
    TIKTOK_POST_SCHEMA, TIKTOK_COMMENT_SCHEMA,
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
comment_serializer = AvroSerializer(schema_registry_client,
                                    COMMENT_SCHEMA)
facebook_post_serializer = AvroSerializer(schema_registry_client,
                                          FACEBOOK_POST_SCHEMA)
facebook_comment_serializer = AvroSerializer(schema_registry_client,
                                          FACEBOOK_COMMENT_SCHEMA)
instagram_post_serializer = AvroSerializer(schema_registry_client,
                                          INSTAGRAM_POST_SCHEMA)
instagram_comment_serializer = AvroSerializer(schema_registry_client,
                                          INSTAGRAM_COMMENT_SCHEMA)
linkedin_post_serializer = AvroSerializer(schema_registry_client,
                                          LINKEDIN_POST_SCHEMA)
linkedin_comment_serializer = AvroSerializer(schema_registry_client,
                                          LINKEDIN_COMMENT_SCHEMA)
tiktok_post_serializer = AvroSerializer(schema_registry_client,
                                          TIKTOK_POST_SCHEMA)
tiktok_comment_serializer = AvroSerializer(schema_registry_client,
                                          TIKTOK_COMMENT_SCHEMA)

#DESERIALIZER
keyterm_deserializer = AvroDeserializer(schema_registry_client,
                                         KEY_TERM_SCHEMA)
task_deserializer = AvroDeserializer(schema_registry_client,
                                    TASKS_SCHEMA)
post_deserializer = AvroDeserializer(schema_registry_client,
                                    POST_SCHEMA)
comment_deserializer = AvroDeserializer(schema_registry_client,
                                    COMMENT_SCHEMA)
facebook_post_deserializer = AvroDeserializer(schema_registry_client,
                                          FACEBOOK_POST_SCHEMA)
facebook_comment_deserializer = AvroDeserializer(schema_registry_client,
                                          FACEBOOK_COMMENT_SCHEMA)
instagram_post_deserializer = AvroDeserializer(schema_registry_client,
                                          INSTAGRAM_POST_SCHEMA)
instagram_comment_deserializer = AvroDeserializer(schema_registry_client,
                                          INSTAGRAM_COMMENT_SCHEMA)
linkedin_post_deserializer = AvroDeserializer(schema_registry_client,
                                          LINKEDIN_POST_SCHEMA)
linkedin_comment_deserializer = AvroDeserializer(schema_registry_client,
                                          LINKEDIN_COMMENT_SCHEMA)
tiktok_post_deserializer = AvroDeserializer(schema_registry_client,
                                          TIKTOK_POST_SCHEMA)
tiktok_comment_deserializer = AvroDeserializer(schema_registry_client,
                                          TIKTOK_COMMENT_SCHEMA)
