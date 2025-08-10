#!/bin/bash
set -euo pipefail

# Deployment script for the pattern system
# Usage: ./deploy.sh <environment>

ENVIRONMENT=$1
DEPLOY_DIR="/opt/patterns"
CONFIG_DIR="/etc/patterns"
LOG_DIR="/var/log/patterns"

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 <staging|production>"
    exit 1
fi

# Load environment configuration
source "./deploy/config_${ENVIRONMENT}.sh"

echo "Starting deployment to $ENVIRONMENT environment..."

# Create required directories
echo "Creating directories..."
mkdir -p "$DEPLOY_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$LOG_DIR"

# Deploy application files
echo "Deploying application files..."
cp -r src/* "$DEPLOY_DIR/"
cp -r config/* "$CONFIG_DIR/"

# Set correct permissions
echo "Setting permissions..."
chmod -R 755 "$DEPLOY_DIR"
chmod -R 644 "$CONFIG_DIR"
chmod -R 755 "$LOG_DIR"

# Deploy environment-specific configuration
echo "Deploying environment configuration..."
cp "./deploy/config_${ENVIRONMENT}.sh" "$CONFIG_DIR/environment"

# Stop current service if running
if systemctl is-active --quiet pattern-service; then
    echo "Stopping current service..."
    systemctl stop pattern-service
fi

# Start new service
echo "Starting service..."
systemctl start pattern-service

# Verify deployment
echo "Verifying deployment..."
./deploy/health_check.sh "$ENVIRONMENT"

echo "Deployment to $ENVIRONMENT completed successfully"