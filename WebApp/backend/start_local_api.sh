#!/bin/bash

# Script to start the local API with proper layer preparation

# Step 1: Build the commonUtil layer
echo "Building commonUtil layer..."
./build_layer.sh

# Step 2: Start the SAM local API with warm containers
echo "Starting SAM local API with warm containers..."
sam local start-api \
  --template ../../CloudFormation/dev_yaml/template-local.yaml \
  --docker-network task_management_network \

# Note: The --warm-containers EAGER option keeps containers warm to reduce cold start time