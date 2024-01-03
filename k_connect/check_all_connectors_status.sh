#!/bin/bash

echo "Available Connectors are:"
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors | jq

echo "Status:"
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/tiktok-post-sink/status | jq
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/tiktok-comment-sink/status | jq

curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/twitter-post-sink/status | jq
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/twitter-comment-sink/status | jq

curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/linkedin-post-sink/status | jq
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/linkedin-comment-sink/status | jq

curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/facebook-post-sink/status | jq
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/facebook-comment-sink/status | jq

curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/instagram-post-sink/status | jq
curl -s -H 'Content-Type: application/json' http://localhost:8083/connectors/instagram-comment-sink/status | jq
