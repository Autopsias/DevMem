#!/bin/bash
set -euo pipefail

# Traffic routing update script for blue-green deployment
# Usage: ./update_routing.sh <environment> --target=<blue|green> --percentage=<0-100>

ENVIRONMENT=$1
TARGET=""
PERCENTAGE=""

# Parse arguments
while [[ $# -gt 1 ]]; do
    case "$2" in
        --target=*)
            TARGET="${2#*=}"
            shift
            ;;
        --percentage=*)
            PERCENTAGE="${2#*=}"
            shift
            ;;
        *)
            echo "Unknown option: $2"
            exit 1
            ;;
    esac
done

# Validate input
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 <staging|production> --target=<blue|green> --percentage=<0-100>"
    exit 1
fi

if [[ ! "$TARGET" =~ ^(blue|green)$ ]]; then
    echo "Invalid target: $TARGET"
    echo "Must be 'blue' or 'green'"
    exit 1
fi

if ! [[ "$PERCENTAGE" =~ ^[0-9]+$ ]] || [ "$PERCENTAGE" -lt 0 ] || [ "$PERCENTAGE" -gt 100 ]; then
    echo "Invalid percentage: $PERCENTAGE"
    echo "Must be between 0 and 100"
    exit 1
fi

# Load environment configuration
source "./deploy/config_${ENVIRONMENT}.sh"

echo "Updating traffic routing for $ENVIRONMENT ${TARGET} deployment to ${PERCENTAGE}%"

# Configure routing based on environment
if [ "$ENVIRONMENT" = "staging" ]; then
    CONFIG_PATH="/etc/nginx/conf.d/staging"
else
    CONFIG_PATH="/etc/nginx/conf.d/production"
fi

# Create routing configuration
cat > "${CONFIG_PATH}/traffic-split.conf" << EOF
# Traffic split configuration
split_clients "\${request_id}" \$target_backend {
    ${PERCENTAGE}%    ${TARGET};
    *               ${TARGET == "blue" ? "green" : "blue"};
}
EOF

# Reload nginx configuration
if ! nginx -t; then
    echo "Nginx configuration test failed"
    exit 1
fi

systemctl reload nginx

echo "Traffic routing updated successfully"
echo "  - Environment: $ENVIRONMENT"
echo "  - Target: $TARGET"
echo "  - Percentage: $PERCENTAGE%"