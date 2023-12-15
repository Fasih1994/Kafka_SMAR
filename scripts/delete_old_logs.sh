#!/bin/bash

# Specify the folder where log files are located
log_folder="/home/fasih/k_cluster_smar/consumer_logs"

# Find and delete log files older than 15 minutes
find "$log_folder" -name '*.log' -type f -mmin +15 -exec rm {} \;

echo "Old log files deleted."