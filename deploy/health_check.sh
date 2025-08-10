#!/bin/bash
set -euo pipefail

# Health check script for deployed pattern system
# Usage: ./health_check.sh <environment>

ENVIRONMENT=$1
MAX_RETRIES=5
RETRY_DELAY=5

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 <staging|production>"
    exit 1
fi

# Load environment configuration
source "./deploy/config_${ENVIRONMENT}.sh"

# Check service status
check_service() {
    local service_status
    service_status=$(systemctl is-active pattern-service 2>/dev/null || echo "inactive")
    if [[ "$service_status" != "active" ]]; then
        echo "Service not running"
        return 1
    fi
    return 0
}

# Check application health endpoint
check_health_endpoint() {
    local url="${API_URL:-http://localhost:8000}/health"
    local response
    response=$(curl -s "$url" 2>/dev/null || echo '{"status": "unhealthy"}')
    if [[ "$response" != *"healthy"* ]]; then
        echo "Health check failed: $response"
        return 1
    fi
    return 0
}

# Check resource usage
check_resources() {
    local memory_limit=${MAX_MEMORY:-1800}
    local cpu_limit=${MAX_CPU:-80}
    
    # Check memory usage
    local memory_usage
    memory_usage=$(free -m 2>/dev/null | awk '/^Mem:/{print $3}' || echo "0")
    if [[ -n "$memory_usage" && "$memory_usage" -gt "$memory_limit" ]]; then
        echo "Memory usage too high: ${memory_usage}MB"
        return 1
    fi
    
    # Check CPU usage
    local cpu_usage
    cpu_usage=$(top -bn1 2>/dev/null | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}' || echo "0")
    if [[ -n "$cpu_usage" && "${cpu_usage%.*}" -gt "$cpu_limit" ]]; then
        echo "CPU usage too high: ${cpu_usage}%"
        return 1
    fi
    
    return 0
}

# Check logs for errors
check_logs() {
    local log_file="${LOG_DIR:-/var/log/patterns}/pattern-service.log"
    if [[ -f "$log_file" ]] && grep -i "error\|exception\|fatal" "$log_file" >/dev/null 2>&1; then
        echo "Found errors in logs"
        return 1
    fi
    return 0
}

# Main health check loop
echo "Starting health checks for $ENVIRONMENT environment..."
    
    # Run all checks
    checks_passed=true
    
    echo "Checking service status..."
    if ! check_service; then
        checks_passed=false
    fi
    
    echo "Checking health endpoint..."
    if ! check_health_endpoint; then
        checks_passed=false
    fi
    
    echo "Checking resource usage..."
    if ! check_resources; then
        checks_passed=false
    fi
    
    echo "Checking logs..."
    if ! check_logs; then
        checks_passed=false
    fi
    
    if [[ "$checks_passed" == "true" ]]; then
        echo "All health checks passed"
        exit 0
    fi
    
    if [[ "$i" -lt "$MAX_RETRIES" ]]; then
        echo "Some checks failed, retrying in $RETRY_DELAY seconds..."
        sleep "$RETRY_DELAY"
    fi
done

echo "Health checks failed after $MAX_RETRIES attempts"
exit 1