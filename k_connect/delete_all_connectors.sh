#!/bin/bash


curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/twitter-post-sink | jq
curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/twitter-comment-sink | jq

curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/tiktok-post-sink | jq
curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/tiktok-comment-sink | jq

curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/linkedin-post-sink | jq
curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/linkedin-comment-sink | jq

curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/instagram-post-sink | jq
curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/instagram-comment-sink | jq

curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/facebook-post-sink | jq
curl -s -X DELETE -H 'Content-Type: application/json' http://localhost:8083/connectors/facebook-comment-sink | jq