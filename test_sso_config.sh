#!/bin/bash

# Test script for sso-config-generator

echo "Installing sso-config-generator..."
pip install -e .

echo -e "\n=== Testing basic usage ==="
uvx sso-config-generator --help

echo -e "\n=== Testing with different flags ==="
echo "1. Basic usage (dry run):"
uvx sso-config-generator --no-create-directories

echo -e "\n2. With skip-sso-name flag:"
uvx sso-config-generator --skip-sso-name --no-create-directories

echo -e "\n3. With custom role name:"
uvx sso-config-generator --developer-role-name ReadOnlyAccess --no-create-directories

echo -e "\n4. Without OU structure:"
uvx sso-config-generator --no-use-ou-structure --no-create-directories

echo -e "\n5. Testing directory named 'environment':"
mkdir -p test-environment
cd test-environment
uvx sso-config-generator --no-create-directories
cd ..
rm -rf test-environment

echo -e "\n6. Testing validation:"
uvx sso-config-generator --validate

echo -e "\nTests completed."
