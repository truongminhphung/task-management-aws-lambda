#!/bin/bash

# Script to prepare Lambda layer for local testing
echo "Building commonUtil Lambda layer..."

# Create a temporary directory with the right structure
# Lambda Python layers need to be in python/ directory at the root
TEMP_DIR="/tmp/commonUtil_layer"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/python

# Copy the commonUtil directory itself to the python directory
# This ensures imports work as 'import commonUtil'
cp -r $(dirname "$0")/commonUtil $TEMP_DIR/python/

# Create the layer ZIP file
cd $TEMP_DIR
zip -r ../commonUtil_layer.zip .
cd -

# Move the ZIP to the deployment location
mv /tmp/commonUtil_layer.zip $(dirname "$0")/commonUtil_layer.zip

echo "Layer built at: $(dirname "$0")/commonUtil_layer.zip"