#!/bin/bash

# Specify the folder where log files are located
log_folder="/home/fasih/k_cluster_smar/scripts/logs"

# Find and delete empty log files
find "$log_folder" -name '*.log' -type f -size 0 -exec rm {} \;

echo "Empty log files deleted."