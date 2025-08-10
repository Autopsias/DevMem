#!/bin/bash
set -euo pipefail

# Environment configuration script
# Usage: ./configure_environment.sh <environment>

ENVIRONMENT=$1

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 <staging|production>"
    exit 1
fi

# Base configuration
BASE_CONFIG=$(cat << 'EOF'
{
    "service": {
        "name": "pattern-service",
        "version": "1.0.0",
        "log_level": "INFO",
        "metrics_enabled": true,
        "monitoring": {
            "enabled": true,
            "interval": 60,
            "retention_days": 30
        },
        "cache": {
            "enabled": true,
            "max_size": 1000,
            "ttl_seconds": 3600
        }
    },
    "validation": {
        "batch_size": 25,
        "timeout_seconds": 30,
        "retry_count": 3
    },
    "security": {
        "tls_enabled": true,
        "min_tls_version": "1.2",
        "cert_rotation_days": 90
    }
}
EOF
)

# Environment-specific configurations
if [[ "$ENVIRONMENT" == "staging" ]]; then
    CONFIG=$(cat << 'EOF'
{
    "api": {
        "url": "https://api-staging.example.com",
        "rate_limit": 1000,
        "timeout_seconds": 30
    },
    "resources": {
        "max_memory_mb": 1500,
        "max_cpu_percent": 70,
        "worker_count": 10
    },
    "monitoring": {
        "dashboard_url": "https://metrics-staging.example.com",
        "alert_webhook": "https://alerts-staging.example.com/webhook"
    }
}
EOF
)
else
    CONFIG=$(cat << 'EOF'
{
    "api": {
        "url": "https://api.example.com",
        "rate_limit": 5000,
        "timeout_seconds": 30
    },
    "resources": {
        "max_memory_mb": 2000,
        "max_cpu_percent": 80,
        "worker_count": 25
    },
    "monitoring": {
        "dashboard_url": "https://metrics.example.com",
        "alert_webhook": "https://alerts.example.com/webhook"
    }
}
EOF
)
fi

# Create configuration directory (use local path for testing)
mkdir -p "${CONFIG_DIR:-/etc/patterns}"

# Write configurations
echo "$BASE_CONFIG" > "${CONFIG_DIR:-/etc/patterns}/base_config.json"
echo "$CONFIG" > "${CONFIG_DIR:-/etc/patterns}/env_config.json"

# Generate environment file
cat > "./deploy/config_${ENVIRONMENT}.sh" << EOF
# Environment configuration for $ENVIRONMENT
export PATTERN_ENV="$ENVIRONMENT"
export CONFIG_DIR="/etc/patterns"
export API_URL="$(echo "$CONFIG" | grep -o '"url": "[^"]*"' | cut -d'"' -f4)"
export MAX_MEMORY="$(echo "$CONFIG" | grep -o '"max_memory_mb": [0-9]*' | cut -d' ' -f2)"
export MAX_CPU="$(echo "$CONFIG" | grep -o '"max_cpu_percent": [0-9]*' | cut -d' ' -f2)"
export WORKER_COUNT="$(echo "$CONFIG" | grep -o '"worker_count": [0-9]*' | cut -d' ' -f2)"
export DASHBOARD_URL="$(echo "$CONFIG" | grep -o '"dashboard_url": "[^"]*"' | cut -d'"' -f4)"
export ALERT_WEBHOOK="$(echo "$CONFIG" | grep -o '"alert_webhook": "[^"]*"' | cut -d'"' -f4)"
EOF

chmod +x "./deploy/config_${ENVIRONMENT}.sh"

echo "Environment configuration for $ENVIRONMENT completed"