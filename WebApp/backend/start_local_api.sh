#!/bin/bash

# Script to start the local API with proper layer preparation

# Step 1: Build the commonUtil layer
echo "Building commonUtil layer..."
./build_layer.sh

# Step 2: Start the SAM local API
echo "Starting SAM local API..."
sam local start-api \
  --template ../../CloudFormation/dev_yaml/template-local.yaml \
  --docker-network task_management_network

# Note: If you need to pass additional parameters to sam local, 
# you can add them after this script, e.g.:
# ./start_local_api.sh --parameter-overrides Param=Value