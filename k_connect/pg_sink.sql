CREATE SINK CONNECTOR PG_SINK WITH (
'connector.class' = 'io.confluent.connect.jdbc.JdbcSinkConnector',
'connection.url' = 'jdbc:postgresql://10.1.1.15:5432/kafka',
'connection.user' = 'kuser',
'connection.password' = 'poc123',
'topics' = 'calculated_orders_table',
'key.converter' = 'io.confluent.connect.avro.AvroConverter',
'key.converter.schema.registry.url' = 'http://schema-registry:8081',
'value.converter' = 'io.confluent.connect.avro.AvroConverter',
'value.converter.schema.registry.url' = 'http://schema-registry:8081',
'auto.create' = 'true',
'pk.mode' = 'record_value',
'pk.fields' = 'sku_name',
'insert.mode' = 'upsert'
);