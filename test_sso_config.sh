#!/bin/bash

# Test script for sso-config-generator

echo "Installing sso-config-generator..."
uv pip install -e .

echo -e "\n=== Testing basic usage ==="
sso-config-generator --help

echo -e "\n=== Testing version flag ==="
sso-config-generator --version

echo -e "\n=== Testing with different flags ==="
echo "1. Basic usage (dry run):"
sso-config-generator --no-create-directories

echo -e "\n2. With skip-sso-name flag:"
sso-config-generator --skip-sso-name --no-create-directories

echo -e "\n3. With custom role name:"
sso-config-generator --developer-role-name ReadOnlyAccess --no-create-directories

echo -e "\n4. With specific region:"
sso-config-generator --region us-west-2 --no-create-directories

echo -e "\n5. Without OU structure:"
sso-config-generator --no-use-ou-structure --no-create-directories

echo -e "\n6. Testing directory named 'environment':"
mkdir -p test-environment
cd test-environment
sso-config-generator --no-create-directories
cd ..
rm -rf test-environment

echo -e "\n7. Testing validation:"
sso-config-generator --validate

echo -e "\nTests completed."
