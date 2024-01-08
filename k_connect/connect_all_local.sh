#!/bin/bash


MY_IP=$(hostname -I | awk '{print $1}')
DB_NAME="master"
DB_USER="sa"
DB_PASSWORD="Smmartv!0"
DB_PORT=1434
CONNECTION_URL="jdbc:sqlserver://${MY_IP}:${DB_PORT};databaseName=${DB_NAME}"


export CONNECTION_URL
export DB_USER
export DB_PASSWORD

# Get the directory path of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONNECTORS_DIR="${SCRIPT_DIR}/connectors"

# Loop through all shell scripts in the connectors directory and execute them
for connector_script in "${CONNECTORS_DIR}"/*.sh; do
    if [ -f "${connector_script}" ]; then
        sh "${connector_script}"
    fi
done