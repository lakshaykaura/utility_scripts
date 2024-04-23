#!/bin/bash

echo "Enter the source folder:"              # Folder containing JSON request files
read SOURCE_FOLDER

echo "Enter the first endpoint URL:"   # URL for the first endpoint
read ENDPOINT1

echo "Enter the second endpoint URL:"   # URL for the second endpoint
read ENDPOINT2

echo "Enter the directory to store responses for the first endpoint:"           # Directory to store responses for the first endpoint
read RESPONSE_DIR1

echo "Enter the directory to store responses for the second endpoint:"           # Directory to store responses for the second endpoint
read RESPONSE_DIR2

echo "Enter the number of concurrent requests:"                # Number of concurrent requests
read CONCURRENT_REQUESTS

# Ensure response directories exist
mkdir -p "$RESPONSE_DIR1"
mkdir -p "$RESPONSE_DIR2"

# Function to send requests
send_request() {
    local file="$1"
    local response_dir="$2"
    local endpoint="$3"

    local base_filename=$(basename "$file")
    curl -s -m 60 -H "Content-Type: application/json" -d @"$file" "$endpoint" > "$response_dir/$base_filename"
}

export -f send_request

# Send requests in parallel
find "$SOURCE_FOLDER" -type f | xargs -I {} -P $CONCURRENT_REQUESTS bash -c 'send_request "$1" "$2" "$3"' _ {} "$RESPONSE_DIR1" "$ENDPOINT1"
find "$SOURCE_FOLDER" -type f | xargs -I {} -P $CONCURRENT_REQUESTS bash -c 'send_request "$1" "$2" "$3"' _ {} "$RESPONSE_DIR2" "$ENDPOINT2"
