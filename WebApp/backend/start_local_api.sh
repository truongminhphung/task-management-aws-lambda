#!/bin/bash

# Script to start the local API with proper layer preparation

# Step 1: Source environment variables
ENV_FILE="../../CloudFormation/dev_yaml/env.sh"
echo "Loading environment variables from $ENV_FILE..."
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
  echo "Environment variables loaded successfully"
else
  echo "Warning: Environment file not found at $ENV_FILE"
  echo "Using default values from template-local.yaml"
fi

# Step 2: Build the commonUtil layer
echo "Building commonUtil layer..."
./build_layer.sh

# Step 3: Start the SAM local API with warm containers
echo "Starting SAM local API with warm containers..."
sam local start-api \
  --template ../../CloudFormation/dev_yaml/template-local.yaml \
  --docker-network task_management_network \
  --parameter-overrides \
    "DbHost=$DB_HOST \
    DbName=$DB_NAME \
    DbUser=$DB_USER \
    DbPassword=$DB_PASSWORD \
    DbPort=$DB_PORT \
    JwtSecret=$JWT_SECRET" \
    S3BucketName=$S3_BUCKET_NAME \
  --warm-containers EAGER
  
# Note: The --warm-containers EAGER option keeps containers warm to reduce cold start time

# Step 4: Clean up
echo "Cleaning up..."
# Remove the commonUtil layer ZIP file
# rm -f commonUtil_layer.zip
# echo "Local API server stopped."
