## Get plugins
`curl -s -X GET -H 'Content-Type: application/json' http://localhost:8083/connector-plugins | jq '.'`

## Post Connector
`curl -s -X POST -H 'Content-Type: application/json' --data @k_connect/oracle_connector.json http://localhost:8083/connectors | jq`

## Check Connector Status
`curl -s -X GET -H 'Content-Type: application/json' http://localhost:8083/connectors/ORACLE_CDC/status | jq '.'`

## KSQL DB Connect command
`docker exec -it ksqldb-cli ksql http://ksqldb-server1:8088`